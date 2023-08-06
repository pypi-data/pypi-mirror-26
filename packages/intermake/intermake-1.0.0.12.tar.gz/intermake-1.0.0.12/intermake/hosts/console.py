import sys
import traceback
from os import system
from typing import Callable, List, Optional, Tuple, TypeVar, Sequence

import time
from colorama import Back, Fore, Style

from intermake.engine import cli_helper, constants, m_print_helper
from intermake.engine.async_result import AsyncResult
from intermake.engine.constants import EDisplay, EStream, EThread
from intermake.engine.environment import MENV
from intermake.engine.mandate import Mandate
from intermake.engine.plugin import ArgsKwargs, Plugin
from intermake.engine.progress_reporter import IProgressReceiver, ProgressReporter, UpdateInfo
from intermake.hosts.base import ERunMode, PluginHost, RunHostArgs
from intermake.visualisables.visualisable import EColour, IVisualisable, UiInfo
from intermake.visualisables.visualisable_operations import PathToVisualisable
from mhelper import MEnum, exception_helper, file_helper, string_helper
from mhelper.comment_helper import override
from mhelper.exception_helper import SwitchError
#
# CONSTANTS
#
from mhelper.string_helper import FindError


_COLOUR_PROGRESS_SIDE = Style.RESET_ALL + Fore.LIGHTBLACK_EX
_COLOUR_PROGRESS_SPACE_LEFT_ARRAY = []
_COLOUR_PROGRESS_SPACE_LEFT_ARRAY.append( Style.RESET_ALL + Back.RED + Fore.LIGHTRED_EX )
_COLOUR_PROGRESS_SPACE_LEFT_ARRAY.append( Style.RESET_ALL + Back.GREEN + Fore.LIGHTGREEN_EX )
_COLOUR_PROGRESS_SPACE_LEFT_ARRAY.append( Style.RESET_ALL + Back.BLUE + Fore.LIGHTBLUE_EX )
_COLOUR_PROGRESS_SPACE_LEFT_ARRAY.append( Style.RESET_ALL + Back.CYAN + Fore.LIGHTCYAN_EX )
_COLOUR_PROGRESS_SPACE_LEFT_ARRAY.append( Style.RESET_ALL + Back.MAGENTA + Fore.LIGHTMAGENTA_EX )
_COLOUR_PROGRESS_SPACE_LEFT_ARRAY.append( Style.RESET_ALL + Back.YELLOW + Fore.LIGHTYELLOW_EX )

_COLOUR_PROGRESS_POINT = Style.RESET_ALL + Back.WHITE + Fore.BLACK

_COLOUR_PROGRESS_SPACE_RIGHT = Style.RESET_ALL + Back.WHITE + Fore.LIGHTWHITE_EX

# Characters
_CHAR_PROGRESS_SIDE_LEFT = Fore.LIGHTBLACK_EX + "▐"
_CHAR_PROGRESS_SIDE_RIGHT = Fore.LIGHTBLACK_EX + "▌"
_CHAR_PROGRESS_SPACE_LEFT = " "
_CHAR_PROGRESS_SPACE_RIGHT = " "
_CHAR_PROGRESS_POINT = "▌"
_CHAR_COLUMN_SEPARATOR = Style.DIM + " │ " + Style.RESET_ALL

# Sizes
_WIDTH_COLUMN_SEPARATOR = len( _CHAR_COLUMN_SEPARATOR )
_WIDTH_BAR = 20
_WIDTH_CURRENT_ITEM = 40  # was 20
_WIDTH_THREAD = 2
_WIDTH_TITLE = 80  # was 40
_WIDTH_TIME_REMAINING = 10
_WIDTH_CLEAR = _WIDTH_BAR + _WIDTH_COLUMN_SEPARATOR + _WIDTH_TIME_REMAINING

T = TypeVar( "T" )


class EConsoleReport( MEnum ):
    """
    Progress report types.
    
    :data SILENT: No reports
    :data ANSIART: Draw graphical loading
    :data SIMPLE: Literal dump of progress reports
    :data MESSAGES: Only display messages, not generic progress updates
    """
    SILENT = 0
    ANSIART = 1
    SIMPLE = 2
    MESSAGES = 3


class UserExitError( BaseException ):
    """
    Used as a special error to indicate the user wishes to exit. This is always raised past the usual `ConsoleHost` error
    catching, allowing termination of the front-end via the front-end error handler.
    """
    pass


class _ConsoleHostSettings:
    """
    :data console_width        : Width of console for display
    :data clear_screen         : Clear screen between command executions
    :data force_echo           : Always echo the commands
    :data error_traceback      : Print error traceback diagnostics
    """
    
    
    def __init__( self ):
        self.console_width = 80
        self.clear_screen = False
        self.force_echo = True
        self.error_traceback = True  # On by default to make debugging easier!


class ConsoleHostConfiguration:
    """
    :data suppress_errors      : Don't allow raised errors from plugins to escape
    :data print_error_traceback: Print traceback on error
    :data clear_screen         : Clear screen between commands
    :data force_echo           : Echo commands
    :data report               : Reporting mode
    :data use_dot              : Use `.` instead of `_`
    :data keep_results         : Number of results to keep in history
    :data cluster_index        : Index for compute clusters
    :data cluster_count        : Count for compute clusters
    """
    
    
    def __init__( self, run_mode: ERunMode ):
        if run_mode not in (ERunMode.ARG, ERunMode.CLI, ERunMode.PYI, ERunMode.PYS):
            raise SwitchError( "run_mode", run_mode, details = "This run-mode is not supported by ConsoleHost. Did you mean to use a different host?" )
        
        self.run_mode = run_mode
        self.report = EConsoleReport.ANSIART
        self.raise_errors = bool( run_mode not in (ERunMode.ARG, ERunMode.CLI) )
        self.print_errors = bool( run_mode in (ERunMode.ARG, ERunMode.CLI, ERunMode.PYI) )
        self.use_dot = bool( run_mode in (ERunMode.ARG, ERunMode.CLI) )
        self.cluster_index = 0
        self.cluster_count = 1
    
    
    def __str__( self ):
        return "ConsoleHost({})".format( self.run_mode )


class ConsoleHost( PluginHost, IProgressReceiver ):  # this host is always single-threaded so it acts as its own progress receiver
    """
    Hosts plugins in CLI mode
    """
    
    
    def __str__( self ):
        return str( self.console_configuration )
    
    
    @classmethod
    def get_default( cls, run_mode: ERunMode ):
        return cls( ConsoleHostConfiguration( run_mode ) )
    
    
    def _PLUGINHOST_get_run_mode( self ):
        return self.console_configuration.run_mode
    
    
    def _get_console_width( self ):
        return self.console_settings.console_width
    
    
    def translate_name( self, name: str ) -> str:
        return self.translate_name_mode( name, self.__configuration.use_dot )
    
    
    @staticmethod
    def translate_name_mode( name: str, use_dot: bool ):
        char = "." if use_dot else "_"
        text = str( name )
        
        for x in " _-.()":
            text = text.replace( x, char )
        
        for x in "\"'":
            text = text.replace( x, "" )
        
        charchar = char + char
        
        while charchar in text:
            text = text.replace( charchar, char )
        
        text = text.lower()
        
        return text
    
    
    def __init__( self, config: ConsoleHostConfiguration ):
        """
        CONSTRUCTOR
        See the `Core.initialise` function for parameter descriptions.
        """
        super().__init__()
        self.__configuration = config
        self.__settings = None
        self.__pulse = False
        self.__last_message_id = None  # type: Optional[List[int]]
        self.__last_info_depth = None
        self.__last_info_thread_index = None
        self.__browser_path = None
        self.__mandates = []
        self.__last_stream = None
    
    
    @override
    def run_host( self, args: RunHostArgs ):
        """
        Runs the host's main loop.
        """
        run_mode = self.console_configuration.run_mode
        
        if self.console_settings.clear_screen:
            from intermake.plugins.common_commands import cls
            cls()
        
        if cli_helper.print_banner( run_mode ):
            from intermake.plugins import console_explorer
            self.print_message( console_explorer.resultsexplorer_ls(), stream = EStream.INFORMATION )
        
        if run_mode == ERunMode.ARG:
            from intermake.hosts.frontends.command_line import start_cli
            start_cli( args.read_argv )
        elif run_mode == ERunMode.CLI:
            from intermake.hosts.frontends.command_line import start_cli
            start_cli( False )
        elif run_mode == ERunMode.PYI:
            import code
            code.interact( local = MENV.plugins.to_dictionary() )
        elif run_mode == ERunMode.PYS:
            # This host does not "run"
            pass
        else:
            raise SwitchError( "run_mode", run_mode )
    
    
    def get_help_message( self ):
        if self.console_configuration.run_mode == ERunMode.ARG:
            return """
            You are in command-line arguments mode.

            To run a command just pass it as an argument, e.g. for the "eggs" command:

                `$(APPNAME) eggs`

            You can use ? to get help on a command:

                `$(APPNAME) eggs?`

            See that "eggs" takes two arguments, "name" and "good".
            
            You can specify the arguments after the command. We need quotes in BASH or CMD.EXE because our command now contains spaces:

                `$(APPNAME) "eggs Humpty True"`

            You can also name the arguments:

                `$(APPNAME) "eggs good=True"`

            You can also use ? to get help on the last argument:

                `$(APPNAME) "eggs name?"`

            Specify + and - to quickly set boolean arguments:

                `$(APPNAME) "eggs +good"`

            You should use more quotes to pass parameters with spaces:

                `$(APPNAME) "eggs 'Humpty Dumpty'"`
                
            For the list of commands type:
            
                `$(APPNAME) cmdlist`
                
            To start the UI:
            
                `$(APPNAME) ui cli`
                
            Use : to pass multiple commands
            
                `$(APPNAME) cmdlist : ui cli`

            If you don't specify any commands, the CLI UI will start automatically.
            """
        elif self.console_configuration.run_mode == ERunMode.CLI:
            return """
            You are in command-line mode.

            To run a command just type it, e.g. for the "eggs" command:

                `eggs`

            You can use ? to get help on a command:

                `eggs?`

            See that "eggs" takes two arguments, "name" and "good".
            
            You can specify the arguments after the command:

                `eggs Humpty True`

            You can also name the arguments:

                `eggs good=True`

            You can also use ? to get help on the last argument:

                `eggs name?`

            Specify + and - to quickly set boolean arguments:

                `eggs +good`

            You should use quotes to pass parameters with spaces:

                `eggs "Humpty Dumpty"`
                
            For the list of commands type:
            
                `cmdlist`

            This mode is intended for running quick scripts from the command line.
            The Python interfaces provide finer control.
            """
        elif self.console_configuration.run_mode == ERunMode.PYI:
            return """
            You are in Python Interactive mode.

            Run commands like you would in Python, for instance to run the "eggs" command:

                `eggs()`

            Use .help() for help:

                `eggs.help()`

            You have seen that "eggs" takes two arguments, "name" and "good".
            You can use arguments:

                `eggs("Humpty", True)`

            Or named arguments:

                `eggs(name = "Humpty", good = True)`
                
            For the list of commands:
            
                `cmdlist()`

            Notice: This mode puts puts the commands in the global namespace, while useful for interactive sessions, it isn't recommended for Python scripts.
            """
        elif self.console_configuration.run_mode == ERunMode.PYS:
            return """
            You are in Python Script mode.

            You can call commands directly, for instance to run the "eggs" command:

                `from bio42 import commands`
                `commands.eggs()`

            For help on a command use:

                `commands.eggs.help()`
                
            The `cmdlist` command provides the complete list of commands:

                `commands.cmdlist()`

            This mode avoids polluting the global namespace.
            If you are issuing commands interactively, use the PYI mode instead.
            Please see `readme.md` in the application directory for more information.
            """
        else:
            return super().get_help_message()
    
    
    @property
    def console_configuration( self ):
        return self.__configuration
    
    
    @property
    def console_settings( self ) -> _ConsoleHostSettings:
        if self.__settings is None:
            self.__settings = MENV.local_data.store.retrieve( "console", _ConsoleHostSettings )
        
        # noinspection PyTypeChecker
        return self.__settings
    
    
    @property
    def browser_path( self ):
        if self.__browser_path is None:
            root = MENV.root
            
            if root is not None:
                self.__browser_path = PathToVisualisable.root_path( root )
            else:
                self.__browser_path = PathToVisualisable.root_path( _NullRoot() )
        
        return self.__browser_path
    
    
    @browser_path.setter
    def browser_path( self, value ):
        self.__browser_path = value
    
    
    @override
    def call_virtual_run( self, plugin: Plugin, args: ArgsKwargs, callback: Optional[Callable[[AsyncResult], None]], sync: bool ) -> Optional[object]:
        """
        OVERRIDE
        CLI mode just invokes the plugin in the current thread, this means it can return the result verbatim as well.
        """
        host = MENV.host
        
        if not sync:
            if self.console_settings.clear_screen:
                if file_helper.is_windows():
                    system( "cls" )
                else:
                    system( "clear" )
                
                echo = True
            elif self.console_settings.force_echo:
                echo = True
            else:
                echo = False
            
            if echo:
                msg = [constants.COL_CMD + host.translate_name( plugin.name ) + Style.RESET_ALL]
                
                for index, arg in enumerate( args.args ):
                    if index >= len( plugin.args ):
                        raise ValueError( "Cannot invoke plugin «{}» with more arguments ({}: {}) than the plugin takes ({}: {}).".format( plugin, len( args.args ), args.args, len( plugin.args ), plugin.args ) )
                    
                    name = plugin.args[index].name
                    arg = constants.COL_VAL + str( arg ) + Fore.RESET
                    if " " in arg or "\"" in arg:
                        msg.append( Style.DIM + " \"" + name + "=" + arg + "\"" + Style.RESET_ALL )
                    else:
                        msg.append( Style.DIM + " " + name + "=" + arg + Style.RESET_ALL )
                
                for name, arg in args.kwargs.items():
                    name = constants.COL_ARG + name + Fore.RESET
                    arg = constants.COL_VAL + str( arg ) + Fore.RESET
                    if " " in arg or "\"" in arg:
                        msg.append( Style.DIM + " \"" + name + "=" + arg + "\"" + Style.RESET_ALL )
                    else:
                        msg.append( Style.DIM + " " + name + "=" + arg + Style.RESET_ALL )
                
                msg.append( Style.RESET_ALL )
                
                self.print_message( "".join( msg ), EStream.ECHO )
        
        title = plugin.name
        progress = ProgressReporter( self, title, self.__configuration.cluster_index, self.__configuration.cluster_count, 0.5 )
        
        try:
            if self.__configuration.cluster_count != 1:
                if plugin.threading() != EThread.UNMANAGED:
                    progress.print( "Multiple processors have been specified but the «{0}» plugin does not support a divided workload.".format( plugin.name ), stream = EStream.WARNING )
            
            mandate = Mandate( host, progress, plugin, args )
            self.__mandates.append( mandate )
            result = plugin.call_virtual_run()
            self.__mandates.pop( -1 )
            self.end_progress_bar()
            async_result = AsyncResult( plugin.name, result, None, None, progress._message_records )
        except UserExitError:
            raise
        except KeyboardInterrupt as ex:
            if sync:
                raise
            
            self.end_progress_bar()
            async_result = AsyncResult( plugin.name, None, ex, traceback.format_exc(), progress._message_records )
            
            host.print_message( "", stream = EStream.SYSTEM )
            host.print_message( Back.YELLOW + Fore.RED + "-------------------------------------------------" + Style.RESET_ALL, stream = EStream.SYSTEM )
            host.print_message( Back.YELLOW + Fore.RED + "- KEYBOARD INTERRUPT - OUTPUT MAY BE INCOMPLETE -" + Style.RESET_ALL, stream = EStream.SYSTEM )
            host.print_message( Back.YELLOW + Fore.RED + "- PRESS CTRL+C AGAIN TO EXIT                    -" + Style.RESET_ALL, stream = EStream.SYSTEM )
            host.print_message( Back.YELLOW + Fore.RED + "-------------------------------------------------" + Style.RESET_ALL, stream = EStream.SYSTEM )
        except Exception as ex:
            self.end_progress_bar()
            async_result = AsyncResult( plugin.name, None, ex, traceback.format_exc(), progress._message_records )
            self.end_progress_bar()
            
            if self.__configuration.print_errors:
                if self.console_settings.error_traceback:
                    host.print_message( Fore.LIGHTRED_EX + "Execution stopped due to error. Printing traceback now because " + constants.COL_CMD + "error_traceback" + Style.RESET_ALL + Fore.LIGHTRED_EX + " is enabled." + Style.RESET_ALL, stream = EStream.SYSTEM )
                    m_print_helper.print_traceback( ex, wordwrap = self.console_settings.console_width )
                else:
                    host.print_message( Style.RESET_ALL + Fore.LIGHTWHITE_EX + Back.RED + exception_helper.exception_to_string( ex ) + Style.RESET_ALL, stream = EStream.SYSTEM )
            
            if self.__configuration.raise_errors or sync:
                raise
        
        if callback:
            callback( async_result )
        elif not sync:
            self.set_last_result( async_result )
        
        return async_result.result
    
    
    def end_progress_bar( self ):
        """
        If the console cursor is still at the end of a progress bar, be done with it and finish the line.
        """
        if self.__last_message_id is not None:
            sys.stdout.write( "⏎\n" )
            sys.stdout.flush()
            self.__last_message_id = None
        else:
            sys.stdout.flush()
    
    
    def print_message( self, message: str, stream: EStream = EStream.PROGRESS ):
        """
        Calling the inbuilt `print` won't place the newline at the end of any progress bar, so we use this to print things in CLI mode.
        This is for internal use only. Plugins should use `MCMD.print` to allow printing in other hosts (e.g. GUI) also.
        """
        if self is not None:
            self.end_progress_bar()
        
        if stream == EStream.INFORMATION:
            prefix = constants.INFOLINE_INFORMATION
            prefix_s = constants.INFOLINE_INFORMATION_CONTINUED
            suffix = ""
        elif stream == EStream.PROGRESS:
            # noinspection SpellCheckingInspection
            prefix = constants.INFOLINE_MESSAGE
            prefix_s = constants.INFOLINE_MESSAGE_CONTINUED
            suffix = ""
        elif stream == EStream.WARNING:
            prefix = constants.INFOLINE_WARNING + Fore.RED + Back.YELLOW
            prefix_s = constants.INFOLINE_WARNING_CONTINUED + Fore.RED + Back.YELLOW
            suffix = Fore.RESET + Back.RESET
        elif stream == EStream.ECHO:
            prefix = constants.INFOLINE_ECHO
            prefix_s = constants.INFOLINE_ECHO
            suffix = ""
        elif stream == EStream.SYSTEM:
            prefix = constants.INFOLINE_SYSTEM
            prefix_s = constants.INFOLINE_SYSTEM_CONTINUED
            suffix = ""
        else:
            raise SwitchError( "stream", stream )
        
        lines = str( message ).split( "\n" )
        
        if stream == EStream.WARNING and len( lines ) == 1:
            for n in range( 0, 4 ):
                print( constants.INFOLINE_WARNING + Fore.LIGHTRED_EX + Back.YELLOW + lines[0] + suffix, file = sys.stderr, end = "\r" )
                sys.stderr.flush()
                time.sleep( 0.05 )
                print( prefix + lines[0] + suffix, file = sys.stderr, end = "\r" )
                sys.stderr.flush()
                time.sleep( 0.05 )
                
            print( "", file = sys.stderr )
        else:
            for index, line in enumerate( lines ):
                if index == 0 and (self is None or self.__last_stream != stream):
                    print( prefix + line + suffix, file = sys.stderr )
                else:
                    print( prefix_s + line + suffix, file = sys.stderr )
        
        if self is not None:
            self.__last_stream = stream
        
        sys.stderr.flush()
    
    
    @override  # IProgressReceiver
    def question( self, message: str, options: Sequence[object] ) -> object:
        """
        Because it's single threaded, the CLI can just ask the question in the console.
        """
        self.end_progress_bar()
        return ask_cli_question( message, options )
    
    
    @override  # IProgressReceiver
    def progress_update( self, info: UpdateInfo ):
        """
        Progress updates in the CLI get printed direct to the console.
        """
        depth = len( info.depth )
        
        # Don't draw the title card progress indicator
        if depth == 1 and info.message is None:
            return
        
        if self.__configuration.report == EConsoleReport.SILENT:
            return
        elif self.__configuration.report == EConsoleReport.SIMPLE:
            self.__draw_simple_progress( info )
        elif self.__configuration.report == EConsoleReport.ANSIART:
            self.__draw_progress_bar( info )
        elif self.__configuration.report == EConsoleReport.MESSAGES and info.message is not None:
            self.print_message( info.message, stream = info.stream )
    
    
    def __draw_simple_progress( self, info: UpdateInfo ):
        depth = len( info.depth )
        
        if info.message is not None:
            self.print_message( info.message, stream = info.stream )  # to std.out
        else:
            indent = constants.INFOLINE_PROGRESS + ("-" * depth if depth > 0 else "")
            indent_s = constants.INFOLINE_PROGRESS_CONTINUED + ("-" * depth if depth > 0 else "")
            
            print( indent + " PROGRESS: text    = {}".format( Fore.CYAN + info.text + Style.RESET_ALL ), file = sys.stderr )
            
            # if info.depth != self.__last_info_depth:
            #    print( indent_s + "         : depth   = {} ({})".format( ", ".join( str( x ) for x in info.depth ), depth ) )
            #    self.__last_info_depth = info.depth
            
            if info.thread_index != self.__last_info_thread_index:
                print( indent_s + "         : thread  = {} / {}".format( info.thread_index, info.num_threads ), file = sys.stderr )
                self.__last_info_thread_index = info.thread_index
            
            if info.value > 0:
                print( indent_s + "         : value   = {} / {}".format( info.value, info.max ), file = sys.stderr )
            
            if info.value_string:
                print( indent_s + "         : value$  = {}".format( info.value_string ), file = sys.stderr )
            
            print( indent_s + "         : passed  = {}".format( string_helper.time_to_string_short( info.total_time ) ), file = sys.stderr )
            
            remain_text = info.format_time( EDisplay.TIME_REMAINING_SHORT )
            
            if remain_text:
                print( indent_s + "         : remain  = {}".format( remain_text ), file = sys.stderr )
        
        sys.stdout.flush()
    
    
    def __draw_progress_bar( self, info: UpdateInfo ):
        if info.message is not None:
            self.print_message( info.message, stream = info.stream )  # to std.out
            return
        
        #
        # Normal progress bar - what do do?
        #
        
        this_message_id = [info.uid] + [info.thread_index]
        this_message_id.extend( info.depth )
        
        if this_message_id == self.__last_message_id or self.__last_message_id is None:
            # Same source as last message - just overwrite it
            print( "\r", end = "", file = sys.stderr )
        elif this_message_id == self.__last_message_id[:-1]:
            # Up one level from last message, don't print anything unless there is progress information
            if not info.value and not info.value_string:
                return
        else:
            # New source - write a new line
            self.end_progress_bar()
        
        self.__last_message_id = this_message_id
        
        #
        # Normal progress bar - text
        #
        
        # THREAD COLUMN
        if info.num_threads != 1:
            col_thread = m_print_helper.ljust( str( info.thread_index ), " ", _WIDTH_THREAD )
        else:
            col_thread = ""
        
        # TITLE COLUMN
        col_title_text = "-" * (len( info.depth ) - 1) + info.text
        col_title = m_print_helper.ljust( col_title_text, " ", _WIDTH_TITLE )
        
        # PROGRESS COLUMN
        col_progress = m_print_helper.ljust( info.format_progress(), " ", _WIDTH_CURRENT_ITEM )
        
        progress_left_col = _COLOUR_PROGRESS_SPACE_LEFT_ARRAY[len( info.depth ) % len( _COLOUR_PROGRESS_SPACE_LEFT_ARRAY )]
        
        # BAR COLUMN
        if info.max > 0:
            val = int( (info.value / info.max) * _WIDTH_BAR )
            
            if 0 <= val < _WIDTH_BAR:
                col_bar = _COLOUR_PROGRESS_SIDE + _CHAR_PROGRESS_SIDE_LEFT + progress_left_col + m_print_helper.ljust( info.value, _CHAR_PROGRESS_SPACE_LEFT, val ) + _COLOUR_PROGRESS_POINT + _CHAR_PROGRESS_POINT + _COLOUR_PROGRESS_SPACE_RIGHT + m_print_helper.rjust( info.max - info.value, _CHAR_PROGRESS_SPACE_RIGHT, (_WIDTH_BAR - val) ) + _COLOUR_PROGRESS_SIDE + _CHAR_PROGRESS_SIDE_RIGHT + Style.RESET_ALL
            elif val == _WIDTH_BAR:
                col_bar = _COLOUR_PROGRESS_SIDE + _CHAR_PROGRESS_SIDE_LEFT + progress_left_col + m_print_helper.cjust( "done", "-", _WIDTH_BAR + len( _CHAR_PROGRESS_POINT ) ) + _COLOUR_PROGRESS_SIDE + _CHAR_PROGRESS_SIDE_RIGHT + Style.RESET_ALL
            else:
                val = _WIDTH_BAR // 2
                col_bar = _COLOUR_PROGRESS_SIDE + _CHAR_PROGRESS_SIDE_LEFT + progress_left_col + m_print_helper.ljust( "?", "?", val ) + _COLOUR_PROGRESS_POINT + "?" + _COLOUR_PROGRESS_SPACE_RIGHT + m_print_helper.rjust( "?", "?", (_WIDTH_BAR - val) ) + _COLOUR_PROGRESS_SIDE + _CHAR_PROGRESS_SIDE_RIGHT + Style.RESET_ALL
        else:
            col_bar = " " * (_WIDTH_BAR + 3)
        
        # TIME COLUMN
        self.__pulse = not self.__pulse
        
        if 0 < info.max != info.value:
            time_remaining = info.estimate_time()[-1]
            time_remaining_prefix = "-"
        else:
            time_remaining = info.total_time  # time elapsed
            time_remaining_prefix = "+"
        
        time_remaining_txt = time_remaining_prefix + string_helper.time_to_string_short( time_remaining, ":" if self.__pulse else " " )
        col_time = Style.DIM + m_print_helper.ljust( time_remaining_txt, " ", _WIDTH_TIME_REMAINING )
        
        # FORMAT EVERYTHING
        text = constants.INFOLINE_PROGRESS + col_thread + _CHAR_COLUMN_SEPARATOR + col_title + _CHAR_COLUMN_SEPARATOR + col_progress + _CHAR_COLUMN_SEPARATOR + col_bar + _CHAR_COLUMN_SEPARATOR + col_time + Style.RESET_ALL + "  "
        
        # PRINT MESSAGE
        print( text, end = "", file = sys.stderr )
        sys.stderr.flush()
    
    
    @override  # IProgressReceiver
    def was_cancelled( self ) -> bool:
        """
        OVERRIDE
        Because it operates in the main thread, progress in the CLI cannot be cancelled externally.
        (However, the user can just press CTRL+C to force an error at any point, we already pick this up and handle it accordingly elsewhere.)
        """
        return False
    
    
    @override
    def _get_mandate( self ) -> Mandate:
        return self.__mandates[-1] if self.__mandates else Mandate.dead_mandate( self )


def ask_cli_question( message: object, options: Sequence[object] ):
    """
    Asks a question in the CLI.
    :param message: Question to ask 
    :param options: List of options (if `None` defaults to (`True`, `False`)), presented using `str`. 
    :return: Selected option. 
    """
    prefix = Fore.WHITE + Back.BLUE + "QUERY<" + Style.RESET_ALL + " "
    message_ = string_helper.prefix_lines( str( message ), prefix + Fore.MAGENTA, Style.RESET_ALL )
    print( message_, file = sys.stderr )
    
    if not options:
        options = True, False
    
    
    def ___namer( x ):
        if x is True:
            return "yes"
        elif x is False:
            return "no"
        else:
            return MENV.host.translate_name( str( x ) )
    
    
    message_ = (Fore.LIGHTBLACK_EX + "|" + Fore.RESET).join( (Fore.GREEN + ___namer( x ) + Fore.RESET) for x in options ) + Fore.RESET
    print( prefix + message_, file = sys.stderr )
    
    while True:
        print( Fore.YELLOW, end = "", file = sys.stderr )
        the_input = input( "QUERY> " ).lower()
        
        try:
            if len( options ) == 1 and options[0] == "*":
                return the_input
            
            result = string_helper.find( source = options,
                                         search = the_input,
                                         namer = ___namer,
                                         detail = "option" )
            
            print( Style.RESET_ALL, end = "", file = sys.stderr )
            
            return result
        except FindError:
            print( Fore.RED + "Invalid option, try again." + Style.RESET_ALL, file = sys.stderr )
            continue


class _NullRoot( IVisualisable ):
    def visualisable_info( self ) -> UiInfo:
        from intermake.hosts.frontends.gui_qt.designer import resources
        
        return UiInfo( name = MENV.abv_name, comment = "", type_name = MENV.name, value = "", colour = EColour.YELLOW, icon = resources.folder )
