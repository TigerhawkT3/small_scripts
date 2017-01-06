import TimeZones

zone = TimeZones.localzone() # get local time zone
localnow = now(zone) # get current local time
min_date = TimeZones.astimezone(
            TimeZones.ZonedDateTime(
                DateTime(2002,1,1), zone),
                    TimeZones.TimeZone("UTC")) # set local minimum date as UTC

if isfile("lastlog.ser")
    lastlog = open("lastlog.ser") do f
        deserialize(f)
    end
else
    lastlog = ""
end

macro R_str(s)
    s
end

type Loot
    datetime::TimeZones.ZonedDateTime
    winner::AbstractString
    interaction::AbstractString
    gainItem::AbstractString
    gainValue::Int64
    lossItem::AbstractString
    lossValue::Int64
end

function ContainerFromLogs(location::AbstractString)
    expression = Regex(R"^\[\d+,(\d+)T(\d+),0,[^@]+@,@,,,System\]" *
                       R"(?:You (didn't win any|spent|discarded|lost|refined" *
                       R"|received|sold|placed a bet of|won)|Items? acquired:|(.*) " *
                       R"(?:has acquired an?|hat eine?n?))" *
                       R" ([0-9,]+ )?(.*)")
    bag = Loot[]
    files = sort([f for f in readdir(location) if f[1:5]=="Chat_"])
    l = length(files)
    for (counter,fname) in enumerate(files)
        #if fname == "Chat_2016-11-06_09-00-00.Log"
            print(STDERR, "Processing ", counter, " out of ", l, "...\r")
            open(joinpath(location, fname)) do f
                for line in eachline(f)
                    m = match(expression, line)
                    if m !== nothing
                        push!(bag, ParseLoot(bag, m.captures...))
                    end
                end
            end
            #break
        #end
    end
    println(STDERR, "\nDone.")
    return bag
end

function totalsByDay(location::AbstractString)
    # this function will look only at totals by day without saving all loot
    expression = Regex(R"^\[\d+,(\d+)T(\d+),0,[^@]+@,@,,,System\]" *
                       R"(?:You (didn't win any|spent|discarded|lost|refined" *
                       R"|received|sold|placed a bet of|won)|Items? acquired:|(.*) " *
                       R"(?:has acquired an?|hat eine?n?))" *
                       R" ([0-9,]+ )?(.*)")
    k = String["Contraband", "Dilithium", "Dilithium Ore", "Energy Credits"]
    bag = Loot[]
    dct = Dict{String,Int64}(key=>0 for key in k)
    day = min_date
    files = sort([f for f in readdir(location) if f[1:5]=="Chat_"])
    l = length(files)
    println("Date", '\t', join(k, '\t'))
    for (counter,fname) in enumerate(files)
        if fname >= lastlog # "Chat_2016-11-04" < fname < "Chat_2016-11-12" 
            print(STDERR, "Processing ", counter, " out of ", l, "...\r")
            open(joinpath(location, fname)) do f
                for line in eachline(f)
                    m = match(expression, strip(line))
                    if m !== nothing
                        loot = ParseLoot(bag, m.captures...)
                        current = TimeZones.floor(loot.datetime, Dates.Day)
                        if day != current
                            if day != min_date
                                println(Dates.format(day, "yyyy-mm-dd"),
                                        '\t', join((dct[key] for key in k), '\t'))
                                bag = Loot[]
                                dct = Dict{String,Int64}(key=>0 for key in k)
                            end
                            day = current
                        end
                        if loot.gainItem in k || loot.lossItem in k
                            if isempty(bag)
                                push!(bag, loot)
                            else
                                bag[1] = loot
                            end
                        end
                        if loot.gainItem in k
                            dct[loot.gainItem] += loot.gainValue
                        end
                        if loot.lossItem in k
                            dct[loot.lossItem] += loot.lossValue
                        end
                    end
                end
            end
            #break
        end
    end
    println(Dates.format(day, "yyyy-mm-dd"), '\t', join((dct[key] for key in k), '\t'))
    println(STDERR, "\nDone.")
    open("lastlog.ser", "w") do f
        serialize(f, files[end])
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::AbstractString,
                   winner::AbstractString, quantity::AbstractString,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    
    quantity = parse(Int, join(c for c in quantity if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::Void,
                   winner::AbstractString, quantity::AbstractString,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    interaction = ""
    quantity = parse(Int, join(c for c in quantity if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::AbstractString,
                   winner::Void, quantity::AbstractString,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    winner = ""
    quantity = parse(Int, join(c for c in quantity if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::AbstractString,
                   winner::AbstractString, quantity::Void,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    quantity = parse(Int, join(c for c in (length(iq) == 2 ? iq[2] : "1") if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::Void,
                   winner::Void, quantity::AbstractString,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    interaction = ""
    winner = ""
    quantity = parse(Int, join(c for c in quantity if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::Void,
                   winner::AbstractString, quantity::Void,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    interaction = ""
    quantity = parse(Int, join(c for c in (length(iq) == 2 ? iq[2] : "1") if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::AbstractString,
                   winner::Void, quantity::Void,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    winner = ""
    quantity = parse(Int, join(c for c in (length(iq) == 2 ? iq[2] : "1") if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end

function ParseLoot(bag::Array{Loot}, d::AbstractString,
                   t::AbstractString, interaction::Void,
                   winner::Void, quantity::Void,
                   item::AbstractString)
    dt = try
        TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone), TimeZones.TimeZone("UTC"))
    catch TimeZones.AmbiguousTimeError
        attempt = TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 1), TimeZones.TimeZone("UTC"))
        if isempty(bag) || bag[end].datetime < attempt
            attempt
        else
            TimeZones.astimezone(TimeZones.ZonedDateTime(DateTime(d*t, "yyyymmddHHMMSS"), zone, 2), TimeZones.TimeZone("UTC"))
        end
    end
    iq = rsplit(item, " x ", limit=2)
    item = rsplit(strip(iq[1], ['!', '.']), " erhalten", limit=2)[1]
    interaction = ""
    winner = ""
    quantity = parse(Int, join(c for c in (length(iq) == 2 ? iq[2] : "1") if c in "0123456789"))
    
    if interaction in ["lost", "placed a bet of", "discarded", "spent"]
        return Loot(dt, winner, interaction, "", 0, item, -quantity)
    elseif interaction == "sold"
        lItem, gain = rsplit(item, " for ", limit=2)
        quantity, item = split(gain, [' ', '\t'], limit=2)
        gValue = parse(Int, join(c for c in quantity if c in "0123456789"))
        return Loot(dt, winner, interaction, item, gValue, lItem, -1)
    elseif interaction == "didn't win any"
        return Loot(dt, winner, interaction, item, 0, "", 0)
    else
        return Loot(dt, winner, interaction, item, quantity, "", 0)
    end
end
#bag = ContainerFromLogs(R"C:\Program Files (x86)\Perfect World Entertainment\Star Trek Online_en_20141221115946\Star Trek Online\Live\logs\GameClient")
#readline()
#print(length(bag))
totalsByDay(R"C:\Program Files (x86)\Perfect World Entertainment\Star Trek Online_en_20141221115946\Star Trek Online\Live\logs\GameClient")



