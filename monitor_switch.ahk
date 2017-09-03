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
count := false
locations := []
slots := []
bank := 0
filename := "locdata.ini"

Loop 10
    slots.Push({"range":[], "padding":0
                ,"numrepetitions":0, "delay":0
                ,"buttons":[]})

Loop 100
    locations.Push([0,0])

; shift-pause to snap to left monitor, alt-pause to right
+Pause::MouseMove, x1, y
!Pause::MouseMove, x2, y

parse_range(s) {
    ; s := "1, 2, 5-9, 2" returns [1, 2, 5, 6, 7, 8, 9, 2]
    numbers := []
    result := StrSplit(s, ",", " `t")
    for i,var in result {
        IfInString, var, - 
        {
            temp := StrSplit(var, "-")
            if (temp[2] > temp[1])
                Loop % temp[2]-temp[1] + 1
                    numbers.Push(A_index+temp[1]-1)
            else
                Loop % temp[1]-temp[2] + 1
                    numbers.Push(temp[1]-A_index+1)
        }
        else
            numbers.Push(var)
    }
    return numbers
}

expand_sequence(range, seq) {
    ; range := [1, 4, 9], seq := "L R" returns ["L", "R", "L"]
    sequence := []
    seq := StrSplit(seq, " ")
    Loop % range.Length() {
        idx := mod(A_index, seq.Length())
        sequence.Push(seq[idx?idx:seq.Length()])
    }
    return sequence
}

save() {
    global locations
    global slots
    global filename
    for idx, lst in locations
        IniWrite, % lst[1] . "," . lst[2], %filename%, locations, %idx%
    for idx, dct in slots
        for k, v in dct {
            if (k=="range" || k=="buttons") {
                val := ""
                for i,s in v
                    val .= s . ","
                v := RTrim(val, ",")
            }
            IniWrite, %v%, %filename%, % "slot" + idx, %k%
        }
}

load() {
    global locations
    global slots
    global filename
    Loop 100 {
        IniRead, val, %filename%, locations, %A_index%
        locations[A_index] := StrSplit(val, ",")
    }
    Loop 10 {
        IniRead, range, %filename%, % "slot" + A_index, range
        IniRead, padding, %filename%, % "slot" + A_index, padding
        IniRead, numrepetitions, %filename%, % "slot" + A_index, numrepetitions
        IniRead, delay, %filename%, % "slot" + A_index, delay
        IniRead, buttons, %filename%, % "slot" + A_index, buttons
        slots[A_index]["padding"] := padding
        slots[A_index]["numrepetitions"] := numrepetitions
        slots[A_index]["delay"] := delay
        slots[A_index]["range"] := StrSplit(range, ",")
        slots[A_index]["buttons"] := StrSplit(buttons, ",")
    }
}

; save a setup of locations, padding, repetitions,
; delay, and button sequence in a chosen slot
create_cycle() {
    global locations
    global slots
    InputBox, slot, Save/load/cancel, Save this in slot 1-10`, cancel`, save data (SAVE)`, or load data (LOAD)?
    if (slot == "SAVE") {
        save()
        return
    }
    if (slot == "LOAD") {
        load()
        return
    }
    if (slot < 1 || slot > 10)
        return
    InputBox, range, Numbers?, Enter a range of locations e.g. "1`, 2`, 5-9`, 2"
    InputBox, padding, Padding time, How many seconds padding around clicks (decimal okay)?
    InputBox, numrepetitions, Repetitions, How many times?
    InputBox, delay, Delay, Pause how many seconds between cycles (decimal okay)?
    InputBox, buttons, Button sequence, Enter a mouse button sequence to repeat`, like "L R R". L=Left`, R=Right`, M=Middle`, X1=Button4`, X2=Button5.
    range := parse_range(range)
    slots[slot] := {"range":range, "padding":padding
                    ,"numrepetitions":numrepetitions, "delay":delay
                    ,"buttons":expand_sequence(range, buttons)}
}

; uses MouseMove and then Click instead of just Click to handle lag
do_slot(num) {
    global interrupted
    global locations
    global slots
    interrupted := false
    InputBox, numrepetitions, Repetitions, How many times?, , , , , , , , % slots[num]["numrepetitions"]
    slots[num]["numrepetitions"] := numrepetitions
    Loop % numrepetitions {
        for i,loc in slots[num]["range"] {
            MouseMove, locations[loc+1][1], locations[loc+1][2]
            Sleep, slots[num]["padding"] * 500
            if interrupted
                return
            Click % slots[num]["buttons"][i]
            Sleep, slots[num]["padding"] * 500
        }
        if (A_index != slots[num]["numrepetitions"]) {
            if interrupted
                return
            Sleep, slots[num]["delay"] * 1000
        }
    }
}

!+Pause::create_cycle()
; alt-esc to abort do_slot mid-cycle
!Esc::interrupted := true

; swap to last swapped location
Pause::
    if count {
        MouseGetPos, tempx, tempy
        if (Abs(tempx-rx2)<5 && Abs(tempy-ry2)<5)
            return
        rx1 := tempx
        ry1 := tempy
        MouseMove, rx2, ry2
    }
    else {
        MouseGetPos, tempx, tempy
        if (Abs(tempx-rx1)<5 && Abs(tempy-ry1)<5)
            return
        rx2 := tempx
        ry2 := tempy
        MouseMove, rx1, ry1
    }
    count := !count
    return

; Ctrl+Shift+NumpadNumber to save a hotspot
; Ctrl+NumpadNumber to go to or click a hotspot

MoveLocation(ID) {
    global locations
    global bank
    MouseMove, locations[10*bank+ID+1][1], locations[10*bank+ID+1][2]
}

SaveLocation(ID) {
    MouseGetPos, x, y
    global locations
    global bank
    locations[10*bank+ID+1] := [x, y]
}

; with numlock on, ctrl-shift-button to save,
; ctrl-button to go to location
^NumpadIns::SaveLocation(0)
^Numpad0::MoveLocation(0)
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
;^NumpadDel::SaveLocation(11)
;^NumpadDot::MoveLocation(11)

; with numlock on, alt-button to switch bank,
; alt-shift-button to run saved slot
; using tilde (~) to avoid blocking entry of character alt-codes
!NumpadIns::do_slot(10)
~!Numpad0::bank := 0
!NumpadEnd::do_slot(1)
~!Numpad1::bank := 1
!NumpadDown::do_slot(2)
~!Numpad2::bank := 2
!NumpadPgDn::do_slot(3)
~!Numpad3::bank := 3
!NumpadLeft::do_slot(4)
~!Numpad4::bank := 4
!NumpadClear::do_slot(5)
~!Numpad5::bank := 5
!NumpadRight::do_slot(6)
~!Numpad6::bank := 6
!NumpadHome::do_slot(7)
~!Numpad7::bank := 7
!NumpadUp::do_slot(8)
~!Numpad8::bank := 8
!NumpadPgUp::do_slot(9)
~!Numpad9::bank := 9

; mousewheel version for basic mice
; ~MButton & WheelUp::
;     Send {Esc}
;     MouseMove, x1, y
;     return
; ~MButton & WheelDown::
;     Send {Esc}
;     MouseMove, x2, y
;     return