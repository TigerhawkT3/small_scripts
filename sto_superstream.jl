import TimeZones

function GetTotals()
    zone = TimeZones.localzone() # get local time zone
    min_date = TimeZones.astimezone(
                TimeZones.ZonedDateTime(
                    DateTime(2002,1,1), zone),
                        TimeZones.TimeZone("UTC")) # set local minimum date as UTC
    day = min_date
    k = String["Contraband", "Dilithium", "Dilithium Ore", "Energy Credits"]
    dct = Dict{String,Int64}(key=>0 for key in k)
    files = sort([f for f in readdir() if f[1:5]=="Chat_"])
    l = length(files)

    if isfile("lastlog.txt")
        lastlog = open("lastlog.txt") do f
            readstring(f)
        end
    else
        lastlog = ""
    end

    println("Date", '\t', join(k, '\t'))
    for (counter,fname) in enumerate(files)
        if fname >= lastlog # "Chat_2016-11-04" < fname < "Chat_2016-11-12" 
            print(STDERR, "Processing ", counter, " out of ", l, "...\r")
            open(fname) do f
                for line in eachline(f)
                    if length(line) > 70 && line[27:70] == ",0,NumericReceived@,@,,,System]You received " &&
                        (contains(line, "Dilithium") || contains(line, "Energy Credits"))
                        quantity,item = split(strip(line)[71:end], ' '; limit=2)
                        quantity = parse(Int, replace(quantity, ",", ""))
                        if item == "Refined Dilithium"
                            item = "Dilithium"
                        end
                    elseif length(line) > 66 && line[27:66] == ",0,NumericReceived@,@,,,System]You sold "
                        item = "Energy Credits"
                        quantity = parse(Int, replace(rsplit(line, ' '; limit=4)[2], ",", ""))
                    elseif length(line) > 78 && line[27:78] == ",0,NumericConversionSuccess@,@,,,System]You refined "
                        item = "Dilithium"
                        quantity = parse(Int, replace(line[79:end-13], ",", ""))
                    elseif length(line) > 63 && (line[27:56] == ",0,NumericLost@,@,,,System]You" &&
                            (line[57:62] == " lost " || line[57:63] == " spent ") && 
                          (contains(line, "Dilithium") || contains(line, "Energy Credits")))
                        quantity,item = split(strip(line[63:end]), ' '; limit=2)
                        quantity = -parse(Int, replace(quantity, ",", ""))
                        if item == "Refined Dilithium"
                            item = "Dilithium"
                        end
                    elseif length(line) > 83 && line[27:83] == ",0,ItemReceived@,@,,,System]Items acquired: Contraband x "
                        quantity = parse(Int, replace(rsplit(line[71:end], ' ', limit=2)[2], ",", ""))
                        item = "Contraband"
                    elseif length(line) > 79 && line[27:79] == ",0,ItemReceived@,@,,,System]Item acquired: Contraband"
                        quantity = 1
                        item = "Contraband"
                    else
                        continue
                    end
                    dt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(line[12:19]*line[21:26], "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
                    
                    current = TimeZones.floor(dt, Dates.Day)
                    if day != current && day != min_date
                        println(Dates.format(day, "yyyy-mm-dd"),
                                '\t', join((dct[key] for key in k), '\t'))
                        dct = Dict{String,Int64}(key=>0 for key in k)
                    end
                    day = current
                    if item in keys(dct)
                        dct[item] += quantity
                    end
                end
            end
        end
    end
    println(Dates.format(day, "yyyy-mm-dd"), '\t', join((dct[key] for key in k), '\t'))
    println(STDERR, "\nDone.")
    last = files[end][6:15]
    current = files[end]
    for fname in files[end:-1:1]
        current = fname
        if fname[6:15] != last
            break
        end
    end
    open("lastlog.txt", "w") do f
        write(f, current)
    end
end

GetTotals()