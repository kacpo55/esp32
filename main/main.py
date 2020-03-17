
import _thread
import accesspoint
import states


_thread.start_new_thread(states.checkState, ())
_thread.start_new_thread(accesspoint.makeAccesspoint, ())





