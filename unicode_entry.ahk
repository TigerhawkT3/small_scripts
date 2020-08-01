:?:`;u::
    Input, keys, , `;
    if (StrLen(keys) < 5)
        Send {U+%keys%}
    else {
        keys := "0x" + keys
        num := keys - 0x10000
        w1 := Format("{:x}", (num >> 10) + 0xD800)
        w2 := Format("{:x}", (num & 1023) + 0xDC00)
        Send {U+%w1%}{U+%w2%}
    }
    return