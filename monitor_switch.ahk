#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
CoordMode, Mouse, Screen
SetDefaultMouseSpeed, 0
SysGet, TotalWidth, 78
SysGet, TotalHeight, 79
SysGet, monitors, MonitorCount
offset := TotalWidth // monitors
start := offset // 2
x1 := start + offset * 0
x2 := start + offset * 1
y := TotalHeight // 2
rx1 := x1
ry1 := y
rx2 := x2
ry1 := y
count := 0
locations := []

Loop 11 {
    locations.Push([0,0])
}

; shift-pause to snap to left monitor, alt-pause to right
+Pause::MouseMove, x1, y
!Pause::MouseMove, x2, y

; click at a locations, b padding, c times, d delay, e button
; uses MouseMove and then Click instead of just Click at the coords,
; because MouseMove can handle expressions but Click can't
CycleThrough() {
    global locations
    global interrupted
    InputBox, numbuttons, Buttons, Which saved buttons (e.g. 11 for 1-11)?
    InputBox, padding, Padding time, How many seconds padding around clicks (decimal okay)?
    InputBox, numrepetitions, Repetitions, How many times?
    InputBox, delay, Delay, Pause how many seconds between cycles (decimal okay)?
    InputBox, mbutton, Left/Right, Which mouse button? L=Left (default)`, R=Right`, M=Middle`, X1=Button4`, X2=Button5.(default is Left)?
    interrupted := false
    Loop % numrepetitions {
        Loop % numbuttons {
            MouseMove, locations[A_index][1], locations[A_index][2]
            Sleep, padding * 500
            if (interrupted)
                break
            Click %mbutton%
            Sleep, padding * 500
        }
        if (A_index != numrepetitions) {
            if (interrupted)
                break
            Sleep, delay * 1000
        }
    }
    return
}

!+Pause::CycleThrough()
; alt-esc to abort CycleThrough mid-cycle
!Esc::interrupted := true

; swap to last swapped location
Pause::
    if (count) {
        MouseGetPos, tempx, tempy
        if (Abs(tempx-rx2)<5 && Abs(tempy-ry2)<5) {
            return
        }
        rx1 := tempx
        ry1 := tempy
        MouseMove, rx2, ry2
        count--
    }
    else {
        MouseGetPos, tempx, tempy
        if (Abs(tempx-rx1)<5 && Abs(tempy-ry1)<5) {
            return
        }
        rx2 := tempx
        ry2 := tempy
        MouseMove, rx1, ry1
        count++
    }
    return

; Ctrl+Shift+NumpadNumber to save a hotspot
; Ctrl+NumpadNumber to go to or click a hotspot

MoveLocation(ID) {
    global locations
    MouseMove, locations[ID][1], locations[ID][2]
}

SaveLocation(ID) {
    MouseGetPos, x, y
    global locations
    locations[ID] := [x, y]
}

^NumpadEnd::SaveLocation(1)
^Numpad1::MoveLocation(1)
^NumpadDown::SaveLocation(2)
^Numpad2::MoveLocation(2)
^NumpadPgDn::SaveLocation(3)
^Numpad3::MoveLocation(3)
^NumpadLeft::SaveLocation(4)
^Numpad4::MoveLocation(4)
^NumpadClear::SaveLocation(5)
^Numpad5::MoveLocation(5)
^NumpadRight::SaveLocation(6)
^Numpad6::MoveLocation(6)
^NumpadHome::SaveLocation(7)
^Numpad7::MoveLocation(7)
^NumpadUp::SaveLocation(8)
^Numpad8::MoveLocation(8)
^NumpadPgUp::SaveLocation(9)
^Numpad9::MoveLocation(9)
^NumpadIns::SaveLocation(10)
^Numpad0::MoveLocation(10)
^NumpadDel::SaveLocation(11)
^NumpadDot::MoveLocation(11)

; mousewheel version for basic mice
~MButton & WheelUp::
    Send {Esc}
    MouseMove, x1, y
    return
~MButton & WheelDown::
    Send {Esc}
    MouseMove, x2, y
    return