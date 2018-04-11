while (1) {
    $d = "`r                                             `r"
    $d += (get-date | out-string).trim()
    write-host -nonewline $d
    start-sleep -seconds 10
}