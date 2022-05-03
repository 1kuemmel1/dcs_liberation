-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- configuration file for the CTLD Plugin including the JTAC Autolase
--
-- This configuration is tailored for a mission generated by DCS Liberation
-- see https://github.com/dcs-liberation/dcs_liberation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function spawn_crates()
    --- CrateSpawn script which needs to be run after CTLD was initialized (3s delay)
    env.info("DCSLiberation|CTLD plugin - Spawn crates")
    for _, crate in pairs(dcsLiberation.Logistics.crates) do
        ctld.spawnCrateAtZone(crate.coalition, tonumber(crate.weight), crate.zone)
    end
end

function preload_troops(preload_data)
    --- Troop loading script which needs to be run after CTLD was initialized (5s delay)
    env.info(string.format("DCSLiberation|CTLD plugin - Preloading Troops into %s", preload_data["unit"]))
    ctld.preLoadTransport(preload_data["unit"], preload_data["amount"], true)
end

-- CTLD plugin - configuration
if dcsLiberation then
    local ctld_pickup_smoke = "none"
    local ctld_dropoff_smoke = "none"

    -- JTACAutoLase specific options
    local autolase = false
    local smoke = false
    local fc3LaserCode = false

    -- retrieve specific options values
    if dcsLiberation.plugins then
        if dcsLiberation.plugins.ctld then
            env.info("DCSLiberation|CTLD plugin - Setting Up")
            --- Debug Settings
            ctld.Debug = dcsLiberation.plugins.ctld.debug
            ctld.Trace = dcsLiberation.plugins.ctld.debug

            -- Sling loadings settings
            ctld.enableCrates = true
            ctld.slingLoad = dcsLiberation.plugins.ctld.slingload
            ctld.staticBugFix = not dcsLiberation.plugins.ctld.slingload

            --- Special unitLoad Settings as proposed in #2174
            ctld.maximumDistanceLogistic = 300
            ctld.unitLoadLimits = {}
            ctld.unitActions = {}
            for _, transport in pairs(dcsLiberation.Logistics.transports) do
                ctld.unitLoadLimits[transport.aircraft_type] = tonumber(transport.cabin_size)
                ctld.unitActions[transport.aircraft_type] = { crates = transport.crates, troops = transport.troops }
            end

            if dcsLiberation.plugins.ctld.smoke then
                ctld_pickup_smoke = "blue"
                ctld_dropoff_smoke = "green"
            end

            -- Definition of spawnable things
            local ctld_troops = ctld.loadableGroups
            ctld.loadableGroups = {
                { name = "Liberation Troops (2)", inf = 2 },
                { name = "Liberation Troops (4)", inf = 4 },
                { name = "Liberation Troops (6)", inf = 4, mg = 1, at = 1 },
                { name = "Liberation Troops (10)", inf = 5, mg = 2, at = 2, aa = 1 },
                { name = "Liberation Troops (12)", inf = 6, mg = 2, at = 2, aa = 2 },
                { name = "Liberation Troops (24)", inf = 12, mg = 4, at = 4, aa = 3, jtac = 1 },
            }
            if dcsLiberation.plugins.ctld.tailorctld then
                --- remove all default CTLD spawning settings
                --- so that we can tailor them for the tasked missions
                ctld.enableSmokeDrop = false
                ctld.enabledRadioBeaconDrop = false
                ctld.spawnableCrates = {}
                ctld.vehiclesForTransportRED = {}
                ctld.vehiclesForTransportBLUE = {}
                ctld.transportPilotNames = {}
                ctld.logisticUnits = {}
                ctld.pickupZones = {}
                ctld.dropOffZones = {}
                ctld.wpZones = {}
            else
                --- append the default CTLD troops
                for _, troop in pairs(ctld_troops) do
                    table.insert(ctld.loadableGroups, troop)
                end
            end

            --- add all carriers as pickup zone
            if dcsLiberation.Carriers then
                for _, carrier in pairs(dcsLiberation.Carriers) do
                    table.insert(ctld.pickupZones, { carrier.unit_name, ctld_pickup_smoke, -1, "yes", 0 })
                end
            end

            --- generate mission specific spawnable crates
            local spawnable_crates = {}
            for _, crate in pairs(dcsLiberation.Logistics.spawnable_crates) do
                table.insert(spawnable_crates, { weight = tonumber(crate.weight), desc = crate.unit, unit = crate.unit })
            end
            ctld.spawnableCrates["Liberation Crates"] = spawnable_crates

            --- Parse the LogisticsInfo for the mission
            for _, item in pairs(dcsLiberation.Logistics.flights) do
                for _, pilot in pairs(item.pilot_names) do
                    table.insert(ctld.transportPilotNames, pilot)
                    if item.preload then
                        local amount = ctld.unitLoadLimits[item.aircraft_type]
                        timer.scheduleFunction(preload_troops, { unit = pilot, amount = amount }, timer.getTime() + 5)
                    end
                end
                if item.pickup_zone then
                    table.insert(ctld.pickupZones, { item.pickup_zone, ctld_pickup_smoke, -1, "yes", tonumber(item.side) })
                end
                if item.drop_off_zone then
                    table.insert(ctld.dropOffZones, { item.drop_off_zone, ctld_dropoff_smoke, tonumber(item.side) })
                end
                if item.target_zone then
                    table.insert(ctld.wpZones, { item.target_zone, "none", "yes", tonumber(item.side) })
                end
                if dcsLiberation.plugins.ctld.logisticunit and item.logistic_unit then
                    table.insert(ctld.logisticUnits, item.logistic_unit)
                end
            end

            autolase = dcsLiberation.plugins.ctld.autolase
            env.info(string.format("DCSLiberation|CTLD plugin - JTAC AutoLase enabled = %s", tostring(autolase)))

            if autolase then
                smoke = dcsLiberation.plugins.ctld.jtacsmoke
                env.info(string.format("DCSLiberation|CTLD plugin - JTACAutolase smoke = %s", tostring(smoke)))

                fc3LaserCode = dcsLiberation.plugins.ctld.fc3LaserCode
                env.info(string.format("DCSLiberation|CTLD plugin - JTACAutolase fc3LaserCode = %s", tostring(fc3LaserCode)))

                -- JTAC Autolase configuration code
                for _, jtac in pairs(dcsLiberation.JTACs) do
                    env.info(string.format("DCSLiberation|JTACAutolase - setting up %s", jtac.dcsGroupName))
                    if fc3LaserCode then
                        -- If fc3LaserCode is enabled in the plugin configuration, force the JTAC
                        -- laser code to 1113 to allow lasing for Su-25 Frogfoots and A-10A Warthogs.
                        jtac.laserCode = 1113
                    end
                    ctld.JTACAutoLase(jtac.dcsGroupName, jtac.laserCode, smoke, 'vehicle', nil, { freq = jtac.radio, mod = jtac.modulation, name = jtac.dcsGroupName })
                end
            end
            if dcsLiberation.plugins.ctld.airliftcrates then
                timer.scheduleFunction(spawn_crates, nil, timer.getTime() + 3)
            end
        end
    end
end
