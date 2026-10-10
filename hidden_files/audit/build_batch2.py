#!/usr/bin/env python3
"""Batch 2 audit output builder: articles index 10-19."""
import json

ARTICLES = {}

ARTICLES["germany-gcap-fighter-uk-switch"] = {
"corrections": [
    "Kept original angle; verified Oct 8 Burnham-Merz Berlin meeting and 'seek to progress' quote via Reuters.",
    "Added verified context: Politico Oct 4 exploratory-talks report (UK-initiated), German ministry's 'initial coordination talks' confirmation.",
    "Added verified FCAS collapse details (June 2026, Dassault-Airbus workshare/IP dispute, combat cloud survives).",
    "Added verified German objections (maritime-shaped requirements, workshare, BAE/Eurofighter history) and Sweden-Spain alternative / Team Gen 6.",
    "Added verified GCAP context: 2035 target, Canada observer July 2026, Saudi interest, cost-sharing motive.",
],
"sourcesChecked": ["Reuters", "Politico", "The Aviationist", "Breaking Defense (original)"],
"unverifiable": [],
"content": """Britain is pressing ahead with talks that could bring Germany into the Global Combat Air Programme, the sixth-generation fighter it is developing with Italy and Japan, after the collapse of the rival Franco-German FCAS project left Berlin hunting for a new path to a future fighter.

British Prime Minister Andy Burnham raised the idea directly with German Chancellor Friedrich Merz during his first visit to Berlin on Oct. 8. "I've indicated to the Chancellor ... our openness to Germany joining GCAP," Burnham told reporters at the German Chancellery. "That is something that we seek to progress in the coming period, working with our other partners, Italy and Japan."

## Exploratory contacts, not negotiations

The contacts are at an early stage. Politico reported on Oct. 4, citing British and German officials and internal German government documents, that the discussions were initiated by London and cover potential cooperation including industrial workshare and Germany's military capability requirements.

Germany's defense ministry has confirmed only "initial coordination talks" on sixth-generation requirements. Aerospace press reports say the two countries' defense ministers have been tasked with examining potential cooperation, but Berlin stresses that no decision — not even a preliminary commitment — has been made.

## Why Berlin is hesitating

Internal German assessments are skeptical. According to Politico, three objections recur: GCAP is shaped by the maritime requirements of island nations — Britain and Japan — rather than the continental air campaign Germany plans for; winning a fair industrial share in a program whose structure is already settled would be difficult; and the documents reference negative experiences with BAE Systems during the Eurofighter Typhoon program.

Berlin is also studying a different route — a partnership with Sweden and Spain that the internal papers reportedly favor. After FCAS collapsed, eight German companies formed "Team Gen 6" to keep sovereign combat-aircraft expertise alive while the government decides which partnership to pursue.

## The FCAS wreckage

The Future Combat Air System formally ended in June 2026 after nine years of deadlock between Dassault Aviation and Airbus Defence and Space over design authority, workshare and intellectual property, with Dassault reportedly demanding up to 80 percent of the fighter work. Only the program's combat-cloud networking element survived the breakup.

The collapse left the German Air Force without a jointly funded successor to the Eurofighter Typhoon — and left GCAP, targeting service entry around 2035, as the only funded sixth-generation fighter program outside the United States with its industrial structure already in place.

## What London wants from Berlin

For Britain, German participation would share costs at a time of budget strain and validate GCAP as Europe's answer after FCAS. Italy has previously said it is open to new members to help share costs; Japan may need convincing. GCAP has already grown once: Canada signed on as an observer in July, a possible path to deeper engagement, and Saudi Arabia has long been named as a potential partner.

But industry executives warn that new partners can bring delays, and one British defense figure noted that GCAP's timeline is fixed — anyone joining now boards a program whose seats and workshare are largely allocated. For Berlin, the question is whether a seat on that train is better than building a new one with Stockholm and Madrid.""",
}

ARTICLES["arizona-desert-counter-drone-centcom-lessons"] = {
"corrections": [
    "MAJOR REFRAME: original presented the Arizona tests as shaping CENTCOM's Middle East counter-drone fight. Verified sources (army.mil, defence-blog, DVIDS) show Falcon Peak 26.2 is a USNORTHCOM/JIATF-401 exercise focused on the U.S. southern border and homeland defense — rewritten around verified facts.",
    "Added verified specifics: Falcon Peak 26.2 dates (Sept 2026, Yuma), JIATF-401 (est. Aug 2025), 378 incursions in 30 days, permanent three-lane test setup, Lattice baseline, Bullfrog gun, Perseus Harpe interceptor, Acting SecArmy Adam Telle Sept 24 visit.",
    "Dropped unverified CENTCOM-feed claims.",
],
"sourcesChecked": ["U.S. Army (army.mil)", "DVIDS", "Defence-Blog", "Army Recognition", "SOFX/DefenseScoop"],
"unverifiable": ["Original claim that Arizona trials 'feed directly into CENTCOM defenses' — no source found; reframed to verified NORTHCOM/border mission."],
"content": """YUMA PROVING GROUND, Ariz. — For most of September, the desert here echoed with a new kind of arms race: small drones buzzing overhead, and the guns, jammers and interceptor missiles trying to knock them down.

The exercise was Falcon Peak 26.2, the fourth iteration of the counter-drone experimentation campaign and the first held at Yuma. Run by Joint Interagency Task Force 401 — the Pentagon office created in August 2025 to coordinate counter-drone efforts across the military and other agencies — it put systems from multiple vendors through scenarios modeled on the drone incursions plaguing the U.S. southern border.

## A border problem driving the testing

The numbers explain the urgency. The U.S. military detected 378 drone incursions along the U.S.-Mexico border in a single recent 30-day period. Most involve small commercial quadcopters flown by transnational cartels for reconnaissance, smuggling coordination and trafficking — cheap aircraft with tiny radar signatures that conventional air defenses struggle to track, let alone engage without risking collateral damage near populated areas.

Joint Task Force Southern Border logged nearly 400 such incursions in one 30-day stretch, officials said. The mismatch — hundred-dollar drones against million-dollar defenses — is the cost-exchange problem now defining the counter-drone fight, and the reason the Pentagon wants interceptors that cost hundreds, not hundreds of thousands, per shot.

## Permanent lanes, real conditions

Falcon Peak set up three permanent test lanes at Yuma: one for detection sensors, one for electronic defeat, one for kinetic weapons. The Army says the lanes will stay in place for ongoing testing with the Department of War, military units, industry and partners. Yuma has now been designated the primary dedicated interagency counter-small-UAS test and training range — "the blueprint" to be replicated at other ranges, in the words of one Army capability integrator.

This iteration was also the first to use Anduril's Lattice autonomous command-and-control software as the baseline for evaluating commercial sensor-to-shooter capabilities — the first deployment of Lattice for test and evaluation. Vendors ran their systems through multiple realistic scenarios in desert heat, dust, wind and glare, the conditions that make Yuma a stand-in for the border's physical challenges.

Among the systems photographed in action: Allen Control Systems' Bullfrog robotic gun turret firing at drone targets on Sept. 9, and Perseus Defense's Harpe interceptor — a 61 cm missile with a stated 2 km engagement range, launched from a portable launcher weighing under 36 kg — evaluated as a lower-cost kinetic option for use where collateral-damage constraints rule out conventional air-defense weapons.

The exercise drew the Army's top leadership, with Acting Secretary of the Army Adam Telle visiting for Distinguished Visitors Day on Sept. 24.

## The layered answer

Separately, JIATF-401 validated CACI's SkyValor counter-drone system for joint-force use after a June evaluation at Marine Corps Air Station Yuma, with officials calling non-kinetic defeat a crucial layer of border defense.

The lesson from Yuma is blunt: detection comes first — small drones fly low and slow with limited signatures — and no single system solves the problem. The layered answer taking shape is persistent sensors to build the air picture, electronic warfare to jam or take over the threat, and cheap kinetic interceptors for what gets through, all tested in dust and heat until they work.""",
}

ARTICLES["ausa-2026-preview-army-autonomy-drone-command"] = {
"corrections": [
    "Softened original's specific claim of a 'new drone command standing up' — could not verify a formally announced new command; reframed as the Army's autonomy reorganization push.",
    "Added verified AUSA 2026 facts: Oct 12-14 dates, Walter E. Washington Convention Center, 750+ exhibits, confirmed technology themes (autonomy, uncrewed systems, C2, AI, directed energy, long-range fires) via Military Embedded Systems agenda reporting.",
    "Added verified industry exhibits: AM General (next-gen HUMVEE 250hp, autonomous UGV with XTEND NEST, JLTV A2 with Rafael C-UAS), PDW/Booz Allen autonomy software.",
    "Removed 'Defense News will be covering' self-reference.",
],
"sourcesChecked": ["Military Embedded Systems", "PR Newswire (AM General)", "GlobeNewswire", "Breaking Defense (original)"],
"unverifiable": ["Specific claim that a new Army drone command is 'standing up' — no announcement found; described instead as reorganization around uncrewed systems."],
"content": """WASHINGTON — The Association of the U.S. Army opens its 2026 annual meeting on Oct. 12 with the service at an inflection point: new leaders at the top, a sweeping push into autonomy and drones, and hard questions about which modernization programs survive.

The three-day gathering at the Walter E. Washington Convention Center, running Oct. 12-14, is one of North America's largest land-power events — more than 750 exhibits and tens of thousands of attendees, from Army leadership and international delegations to defense contractors and startups.

## Autonomy everywhere

Autonomous and uncrewed systems will be the most visible thread running through the conference. Tuesday's program includes sessions examining the distinction between launched effects and loitering munitions, the integration of autonomy into warfighting, and cooperation with allied partners on uncrewed and counter-uncrewed aircraft systems. Wednesday continues with aviation manned-unmanned teaming and launched effects.

The networks tying it all together get equal billing: data-centric multidomain operations, scaling command and control for the joint fight, interoperability, and an Army C2 acquisition blueprint aimed at accelerating readiness. One session, Project Flytrap, examines a data-centric "kill web" for offensive maneuver — moving information among sensors, commanders and weapons faster than the enemy can react.

After watching drones reshape the war in Ukraine, the Army is reorganizing how it buys, fields and fights with uncrewed systems. The service's autonomy push — from small quadcopters to launched effects fired from helicopters — will dominate both the formal program and the exhibit floor.

## Industry's showcase

AM General will display a redesigned next-generation HUMVEE with a 250-horsepower common-rail diesel engine, a fully autonomous unmanned ground vehicle carrying XTEND's NEST aerial-drone launch pod — letting the vehicle push a drone launch point closer to the fight without putting soldiers at risk — and the JLTV A2 fitted with Rafael drone and counter-drone technology.

Performance Drone Works, the Huntsville drone maker, will hold meetings on mission-autonomy software with Booz Allen that the company says can cut fleet software update cycles from weeks or months to hours, built for operations in denied and degraded connectivity.

Artificial intelligence and cyber operations round out the technology agenda, including a Monday session on AI-enabled cyber defense and critical-infrastructure resilience.

## The budget shadow

Under the technology buzz runs a harder conversation. With budgets under pressure and priorities shifting toward drones, long-range fires and air defense, some legacy modernization efforts face scrutiny from the new leadership.

AUSA is where the Army signals, often bluntly, what it wants to buy — and what it no longer wants. Expect contract announcements, prototype unveilings, and carefully worded warnings to programs falling behind. The conference runs through Oct. 14.""",
}

ARTICLES["uscybercom-cyber-flag-2026-exercise"] = {
"corrections": [
    "Verified all key facts against USCYBERCOM public affairs release via DVIDS: 13th annual, concluded July 31 2026, Suffolk Va., ~3 weeks, 600+ personnel from 20+ nations.",
    "Added verified detail: 6th Multi-National Symposium (July 30-31), Gen. Josh Rudd's triple role (USCYBERCOM/NSA/CSS) and short verified quote.",
    "Expanded with context on cyber mission force and coalition operations without inventing scenario details.",
],
"sourcesChecked": ["U.S. Cyber Command Public Affairs via DVIDS", "U.S. Department of Defense (original source)"],
"unverifiable": [],
"content": """SUFFOLK, Va. — U.S. Cyber Command has concluded its 13th annual Cyber Flag exercise, wrapping nearly three weeks of simulated cyber combat alongside partners and allies from around the world.

The exercise ended July 31, 2026, according to U.S. Cyber Command public affairs. More than 600 personnel from over 20 nations took part, working through simulated malicious cyber threats in a shared digital training environment built to develop a common approach to defending military networks.

## A coalition exercise

Cyber Flag has grown into the premier training event for the U.S. cyber mission force, drawing operators from across the military services and allied nations. This year's iteration closed alongside the command's 6th annual Multi-National Symposium, held July 30-31 and attended by senior officers from more than 20 countries for in-depth discussions on the issues facing an expanding cyber domain.

Army Gen. Josh Rudd — who commands U.S. Cyber Command while also serving as director of the National Security Agency and chief of the Central Security Service — addressed the symposium, stressing that multinational training and preparation are what keep nations ahead of adversaries in pace and capability.

"We never fight as a single service," Rudd said. "As a community, as a nation, as a world, we've never fought alone."

## Why it matters

The training mirrors a daily reality. State-linked hackers probe U.S. and allied military networks constantly, hunting for footholds in everything from weapons systems to logistics networks. Cyber Flag is where defenders rehearse the coordination those attacks demand — across services, agencies and national borders — before a real crisis forces it.

The exercise's scenarios test teams under realistic, high-pressure conditions: defending networks while attacks unfold, sharing threat information across organizational and classification boundaries, and making decisions at the speed the domain requires. As the Pentagon treats cyberspace as a warfighting domain alongside land, sea, air and space, exercises like this one are where the cyber mission force builds the muscle memory for coalition operations.

Cyber Command has not released details of this year's scenarios, citing operational security. What it emphasizes instead is the relationship-building. As Rudd put it, trust is not established during times of crisis — it is built in exercises like Cyber Flag, long before it is needed.""",
}

ARTICLES["zero-trust-weapons-ai-agents-identity"] = {
"corrections": [
    "Verified core claims: 2022 DoD Zero Trust Strategy (91 target outcomes by end FY2027, 61 advanced by FY2032), Strategy 2.0 expected ~Mar 2026 extending to OT/weapons (Randy Resnick), Jan 2026 Implementation Guideline Primer.",
    "Added verified Army agentic-cyber detail via DefenseScoop (task force, kill switch, confidence thresholds, Project Griffin).",
    "Kept original webinar framing but grounded every technical claim in verified Pentagon documents/statements.",
],
"sourcesChecked": ["DoD Zero Trust Strategy documents", "DefenseScoop", "MeriTalk", "Breaking Defense (original)"],
"unverifiable": [],
"content": """WASHINGTON — The Pentagon's Zero Trust cybersecurity drive is entering its hardest phase: pushing identity-based security beyond people and laptops to every weapon system, sensor and AI agent on the network.

Zero Trust assumes no user or device is trustworthy by default, verifying every access request under the principles of "never trust, always verify" and "assume breach." Extending that to weapons is a different order of difficulty. A fighter jet, a missile battery or an AI targeting assistant cannot simply be issued a password — their identities must be baked into hardware and software, resilient to jamming, spoofing and capture.

## From IT to weapons

The original 2022 Defense Department Zero Trust Strategy focused on IT infrastructure, setting 91 cybersecurity capability outcomes that all components must meet to reach target-level Zero Trust by the end of fiscal 2027, with 61 advanced-level outcomes due by fiscal 2032.

The follow-on strategy, expected around March 2026 according to Randy Resnick, senior adviser for the Pentagon's Zero Trust Portfolio Management Office, extends the mandates for the first time to operational technology, internet-of-things systems, defense critical infrastructure and weapons systems: 84 target-level outcomes due by fiscal 2030, plus 21 advanced outcomes by fiscal 2033.

A Zero Trust Implementation Guideline primer published by the department in January 2026 reinforced the approach: continuous authentication and authorization of every user, device and application, rather than reliance on perimeter defenses.

## Why weapons are harder

Operational technology presents challenges that IT-based Zero Trust was never built for. As Resnick has explained, the critical systems controlling water, power and weapons cannot simply be shut down because they are under attack — and legacy operational technology often runs on implicit trust, where security implementations must never override essential safety functions.

The stakes rise as the military networks more of its arsenal together. A single compromised node in a connected force could poison targeting data or blind commanders — exactly what adversaries are trying to achieve.

## AI agents join the identity problem

The identity challenge now extends to software. The Army's cyber command has set up a task force to build agentic cyber tools — AI agents that respond to network threats at machine speed — under an effort that includes a master kill switch to halt autonomous actions within seconds, auditable confidence thresholds and an "undo" function for agent-triggered commands, DefenseScoop reported. If agents roam the network with vulnerabilities, one officer warned, adversaries attacking the agents leaves the force exposed.

Analysts argue organizations should treat AI agents like any other non-human identity, subject to micro-segmentation and continuous monitoring.

Officials describe the identity problem as one of the pacing challenges for the Pentagon's broader digital modernization — the unglamorous work that determines whether the connected force of the 2030s can actually be trusted.""",
}

ARTICLES["navy-commissions-uss-ted-stevens"] = {
"corrections": [
    "CORRECTION: original said the ship 'joins the Pacific Fleet' — verified (navy.mil, DVIDS, Baird Maritime) homeport is Naval Station Norfolk, Virginia, joining the Atlantic Fleet. Fixed.",
    "Verified commissioning date Oct 3, 2026, Whittier Alaska; second Flight III after Jack H. Lucas; SPY-6(V)1 + Aegis Baseline 10.",
    "Added verified build timeline: HII Ingalls Pascagoula, keel Mar 9 2022, launch Aug 15 2023, delivery Dec 29 2025, Norfolk arrival, Panama Canal transit.",
    "Added verified namesake detail: Stevens Senate service Dec 1968-Jan 2009, WWII 'The Hump' C-46/C-47 pilot, Distinguished Flying Cross.",
    "Added verified ceremony detail: Acting SecNav Hung Cao, CO Capt. Mary Katey Hayes, motto 'Lead with Courage', Tlingit 'Woosh-Jee-een'.",
],
"sourcesChecked": ["U.S. Navy (navy.mil)", "DVIDS", "Baird Maritime", "U.S. Department of Defense (original source)"],
"unverifiable": [],
"content": """WHITTIER, Alaska — The U.S. Navy placed its newest guided-missile destroyer, USS Ted Stevens (DDG 128), into active commission on Oct. 3 during a formal ceremony in this deep-water port — an unusual setting that honored both the ship's namesake and Alaska's strategic weight.

The Ted Stevens is the second Flight III Arleigh Burke-class destroyer to enter service, after USS Jack H. Lucas in 2023. Its combat power centers on the Raytheon AN/SPY-6(V)1 Air and Missile Defense Radar — a 3D active electronically scanned array far more sensitive than earlier radars — paired with Lockheed Martin's Aegis Baseline 10 combat system.

## Built for missile defense

The Flight III hull is redesigned around the radar's appetite for power and cooling: three 4,000 kW gas turbine generators and upgraded air-conditioning plants feed the array. The Navy says the upgrade lets the destroyer handle anti-air warfare and ballistic missile defense simultaneously, alongside anti-submarine, anti-surface and strike missions through the Mk 41 vertical launching system.

Demand for missile-defense-capable destroyers continues to outstrip supply among the fleet's combatant commanders.

## From Pascagoula to Alaska

Huntington Ingalls Industries' Ingalls Shipbuilding division built the ship in Pascagoula, Mississippi. The keel was laid March 9, 2022; the ship launched Aug. 15, 2023; and the Navy accepted delivery on Dec. 29, 2025. She departed the yard May 8, 2026, reached Norfolk a week later, then sailed via the Panama Canal to Alaska for commissioning.

After post-commissioning operations, the destroyer will return to her homeport at Naval Station Norfolk, Virginia, joining the Atlantic Fleet.

## The namesake

The ship honors the late Sen. Ted Stevens, who represented Alaska from December 1968 to January 2009. Before politics, he flew C-46 and C-47 transport missions over "The Hump" in the China-Burma-India theater as an Army Air Forces pilot in World War II, earning the Distinguished Flying Cross. He later championed Alaska statehood and, in the Senate, defense spending, Arctic security and military pay and benefits.

Acting Secretary of the Navy Hung Cao delivered the principal address. The ship's commanding officer, Capt. Mary Katey Hayes, told the crew they were ready to answer the nation's call. The motto: "Lead with Courage." In keeping with tradition, the sponsors — Stevens' wife Catherine Ann Stevens and daughters Susan Stevens Covich and Lily Stevens Becker — gave the order to "man our ship and bring her to life."

The Navy noted the Tlingit phrase "Woosh-Jee-een" — "working together" — as the spirit of the partnership among the Navy, the Stevens family, the crew and Alaska. Staging the ceremony in Alaska was itself a statement: the Arctic is becoming a zone of strategic competition, and the commissioning put one of the fleet's most advanced ships on display in the region's waters.""",
}

ARTICLES["air-force-fq42-vengeance-fq44-fury-cca"] = {
"corrections": [
    "Verified naming announcement: Sept 14, 2026, SecAF Troy Meink, AFA Air Space & Cyber Conference, National Harbor (Defense News, The Aviationist).",
    "Added verified program detail: 500 CCAs by 2032 / ~1,000 total; FQ-42A first flight Aug 2025; June 2026 EMD+production contracts; FQ-44A live-fire inert AIM-120 BLOS strike; ~$1B FY2027 request.",
    "Added verified naming color: 'Fury' was Anduril's internal name; 'Dark Merlin' (GA-ASI) replaced by 'Vengeance'.",
    "Corrected designations to FQ-42A / FQ-44A per official usage.",
],
"sourcesChecked": ["Defense News", "The Aviationist", "U.S. Air Force", "U.S. Department of Defense (original source)"],
"unverifiable": [],
"content": """NATIONAL HARBOR, Md. — The Air Force has given names to its future drone wingmen. The service's first two Collaborative Combat Aircraft will be called the FQ-42A Vengeance and the FQ-44A Fury, Secretary of the Air Force Troy Meink announced Sept. 14 during his keynote at the Air & Space Forces Association's Air, Space & Cyber Conference.

The naming is more than ceremony. It marks the CCA program's passage from concept to real hardware with real designations — and Meink paired it with a production target: at least 500 autonomous aircraft in service by 2032, on the way to a planned fleet of about 1,000.

"By then, our special operators will have the ability to employ thousands of autonomous one-way attack systems, and we will have autonomous fighters like the Collaborative Combat Aircraft," Meink said. "They'll perform many of the missions that manned fighters currently execute."

## Two vendors, two aircraft

General Atomics Aeronautical Systems builds the FQ-42A; Anduril Industries builds the FQ-44A. The "FQ" prefix follows Air Force convention — F for fighter, Q for unmanned. The Fury name was already in use inside Anduril; for the FQ-42, the service replaced General Atomics' internal "Dark Merlin" with Vengeance.

The aircraft moved fast. General Atomics' FQ-42A flew for the first time in August 2025, less than 18 months after contract award — "almost unheard of in aircraft development," Meink said. Anduril rolled its first FQ-44A off the assembly line in July 2026 after flight testing that began in October 2025.

In June 2026 the Air Force awarded both companies engineering, manufacturing development and production contracts for Increment 1 — ahead of schedule, after judging both designs ready for full-scale manufacturing. The service requested nearly $1 billion in fiscal 2027 funding to begin procurement, aiming for more than 150 combat-capable aircraft by the end of the decade.

## Tested in combat-relevant missions

The program has already shot live weapons. The Air Force recently completed its first live-fire test with Anduril's FQ-44A: an end-to-end, beyond-line-of-sight strike against a simulated target using an inert AIM-120 missile.

CCAs are designed as affordable, semi-autonomous unmanned aircraft that extend the reach of crewed fighters like the F-35 and the future F-47. They can carry sensors and weapons deep into contested airspace, scout ahead, jam enemy radars or strike targets — with onboard systems handling flight functions while human operators keep the higher-level mission decisions.

The service is already preparing Increment 2, expected to fold in lessons from the first aircraft and expand capabilities — the next step in a program meant to number in the thousands.""",
}

ARTICLES["norad-f16s-arctic-vanguard-high-north"] = {
"corrections": [
    "Verified operation details: Arctic Vanguard 26-4.2, Sept 13-26 2026, Eielson F-16s to Goose Bay, forward deployment into Greenland with Denmark/NATO (globalsecurity.org/DVIDS).",
    "Added verified detail: Lt. Gen. Robert D. Davis quote, Nordic Bridge concept, RCAF CC-177 airlift, KC-135 over Greenland Sept 16, 354th Fighter Wing.",
    "Kept original's note that aircraft numbers/duration undisclosed — matches NORAD statements.",
],
"sourcesChecked": ["GlobalSecurity.org (Alaskan Command PA)", "DVIDS", "Defence-Blog", "U.S. Department of Defense (original source)"],
"unverifiable": [],
"content": """F-16 Fighting Falcons from Eielson Air Force Base, Alaska, have deployed to Goose Bay in Newfoundland and Labrador, Canada, to fly defense missions across the Arctic under Operation Arctic Vanguard 26-4.2.

The operation, running Sept. 13-26, pairs the Alaskan NORAD Region directly with the Canadian NORAD Region to execute what the command calls critical defense missions across the Arctic — the northern approaches an adversary's long-range bombers and cruise missiles would use against North America.

## Beyond Goose Bay

The deployment does not stop in Canada. NORAD personnel and aircraft are to forward deploy into Greenland for operations in austere conditions alongside partners from Denmark and other NATO countries — staging combat airpower from Alaska, through northeastern Canada, to the Greenland ice cap in a single operational sequence.

"Operation Arctic Vanguard demonstrates that austere conditions and vast distances present no barrier to NORAD's collective defense," said Air Force Lt. Gen. Robert D. Davis, commander of the Alaskan NORAD Region. "Deploying combat airpower from Alaska across Canada and forward into Greenland validates our agile combat capabilities."

The operation supports the NORAD and U.S. Northern Command "Nordic Bridge" concept, which aligns the commands' Arctic operations, exercises, training and investments with NATO and regional partners.

## Agile combat, Arctic conditions

The move is a practical test of agile combat employment: can multi-role fighters be shifted rapidly from the Pacific theater, sustained across vast distances, and generated for air-superiority missions in sub-zero, infrastructure-poor environments? Royal Canadian Air Force strategic airlift — including CC-177 Globemaster IIIs loading 354th Fighter Wing cargo at Eielson — supported the deployment, and a KC-135 Stratotanker flew in formation with the F-16s over Greenland on Sept. 16.

The Eielson jets are no strangers to extreme cold, routinely training in Arctic conditions. Operating from Goose Bay extends their reach over the North Atlantic and eastern Arctic.

## Why the High North matters

The Arctic has become a growing security concern. Russia has reopened Cold War-era bases along its northern coast; China calls itself a "near-Arctic state" and keeps expanding its icebreaker fleet. NORAD, the joint U.S.-Canadian command, owns the mission of detecting and intercepting threats across the region.

Arctic Vanguard is part of a recurring series of NORAD and Northern Command operations meant to build presence, practice operating from forward Arctic locations and defend the continent's northern approaches. NORAD has not disclosed how many aircraft are involved or the exact Greenland operating location.""",
}

ARTICLES["b52-lrasm-agm158c-anti-ship-missiles"] = {
"corrections": [
    "Verified the triggering news: Oct 7, 2026 NAVAIR sole-source notice to Lockheed Martin (cost-plus-fixed-fee), scope (software updates, testing, test asset repair, failure review boards), no schedule given.",
    "Verified LRASM facts: AGM-158C, >200nm range, RF/IR + datalink, JASSM-ER derivative, AGM-158C-3 variant; B-1B operational, B-2 capability revealed earlier 2026, F/A-18E/F, F-15/F-35/P-8 in work.",
    "Added verified Gunzinger quote (short) and 'discussed since 2019' history via Naval News/Air & Space Forces Magazine.",
    "Softened 'completing the bomber trio' framing to reflect integration is underway, not yet fielded.",
],
"sourcesChecked": ["The War Zone (original)", "Air & Space Forces Magazine", "Naval News", "Army Recognition"],
"unverifiable": [],
"content": """The B-52 Stratofortress is in line for the AGM-158C Long Range Anti-Ship Missile, after Naval Air Systems Command announced Oct. 7 that it intends to award Lockheed Martin a sole-source contract to integrate the stealthy weapon onto the Air Force's oldest bomber.

The planned cost-plus-fixed-fee delivery order covers LRASM integration on the B-52, including missile software updates, associated testing, repair of test assets and failure review boards. The notice gives no schedule for completing the integration or fielding the capability.

## An arsenal plane for maritime strike

The B-52 can already carry up to 20 AGM-158 Joint Air-to-Surface Standoff Missiles — the family LRASM is derived from, sharing similar dimensions — and the notice does not specify how many LRASMs the bomber would ultimately carry. The idea has circulated since at least 2019, when Naval News first reported the possibility, but languished for years until the current push.

Retired Air Force Col. Mark Gunzinger, a former B-52 pilot now with the Mitchell Institute, told Air & Space Forces Magazine that "a handful of B-52s will be able to deliver more weapons on maritime targets and do so over much longer ranges than the Navy's carrier-based aircraft per day."

## The missile

LRASM is a subsonic, stealthy cruise missile built by Lockheed Martin as a variant of the AGM-158B JASSM-ER. It flies more than 200 nautical miles, using radio-frequency and infrared seekers plus a datalink to find and identify ships autonomously — including when GPS is jammed and datalinks are denied, the conditions expected in a Pacific fight.

The AGM-158C-3 variant, expected to be procured for the first time this fiscal year, adds improved beyond-line-of-sight targeting, better electronic counter-countermeasures and software upgrades.

## Spreading across the force

The B-1B already carries LRASM, and the Air Force revealed earlier this year that the stealthy B-2 can launch it as well — a capability not previously disclosed. Navy F/A-18E/F Super Hornets fly it today; integration is underway for the F-15, the Marine Corps and Navy F-35 variants and the P-8A Poseidon, and the future B-21 is certain to follow.

The move reflects the Pentagon's focus on the Indo-Pacific, where China's navy — now the world's largest by hull count — is the pacing challenge. Holding that fleet at risk from long range, from multiple launch axes, is a central element of U.S. war planning.""",
}

ARTICLES["us-f35-push-portugal-f16-replacement"] = {
"corrections": [
    "Verified Oct 8 Rubio Lisbon visit ('very competitive' offer) and Rangel response via The War Zone; competitor set (Eurofighter, Rafale, Gripen E).",
    "CORRECTION: original said Portugal's F-16s were 'bought second-hand' — replaced with verified Peace Atlantis I/II acquisition history (45 F-16A/B Block 15, first new-build deliveries 1994).",
    "Added verified context: March 2025 shelving over 'allied predictability' concerns; Dassault Rafale offer July 2026 + AED Cluster protocol Sept 23; LM protocol June 2025; no formal tender yet; Military Programming Law pending; 27-28 aircraft ~€5B; fleet figures 25-28 with attribution.",
],
"sourcesChecked": ["The War Zone (original)", "Army Recognition", "Grosswald.org", "Simple Flying"],
"unverifiable": ["Exact current fleet size varies by source (25 per TWZ, 28 F-16M per others) — presented both with attribution."],
"content": """LISBON — The United States is pressing Portugal to choose the F-35 for its next fighter, with Secretary of State Marco Rubio promising Lisbon a "very competitive" American offer during an Oct. 8 visit.

Portuguese Foreign Minister Paulo Rangel, standing alongside Rubio, said the government is seriously considering the F-35A Lightning II — along with the Eurofighter Typhoon, Dassault Rafale and Saab Gripen E — to replace the air force's aging F-16s.

"The Portuguese state will always decide in accordance with the national interest," Rangel said at the news conference. "There is one point that is also clear: we are seriously considering the F-35 proposal, just as we are considering others."

## A 5 billion euro decision

The requirement covers Portugal's fleet of upgraded F-16M fighters — 28 by some counts — with a possible buy of 27 to 28 aircraft valued near 5 billion euros, one of Lisbon's largest planned military investments. The War Zone reports the current operational fleet as 25 modernized F-16AM/BMs — 21 single-seat and four two-seat aircraft — based at Monte Real Air Base.

Portugal acquired 45 F-16A/B Block 15 aircraft through the Peace Atlantis I and II programs, with the first new-build jets delivered from 1994 to equip Esquadra 201 "Falcoes." Whatever Lisbon picks next will anchor its airpower for decades.

## A reopened door

The American push follows a cold spell. In March 2025, Portugal questioned the reliability of long-term U.S. defense commitments — citing "allied predictability" as a fundamental asset — and shelved F-35 plans in favor of European options. The Oct. 8 meeting reopened the prospect of a major American fighter sale.

Competition is already formal. Dassault Aviation submitted a Rafale offer to the Portuguese government and air force in July 2026, then signed a cooperation protocol with the AED Cluster Portugal industry association on Sept. 23 alongside Thales and Safran. Lockheed Martin signed a similar protocol with the same association in June 2025; the Eurofighter consortium and Saab have followed on identical, non-exclusive terms.

## No tender yet

Lisbon has not formally launched a replacement competition. The chief of the defense staff, Gen. Joao Cartaxo Alves — who as air force commander favored the F-35A — has said the F-16 replacement will be written into a new military programming law still to go to parliament; a tender can follow only after adoption, unless the government chooses a government-to-government deal.

For Washington, the stakes go beyond one sale: keeping a NATO ally inside the F-35 ecosystem preserves interoperability, training pipelines and industrial ties for decades. For Lisbon, the choice balances capability, cost and strategic alignment — and, as Rangel made clear, will be decided on national interest.""",
}

# --- assemble output ---
out = {}
for slug, d in ARTICLES.items():
    wc = len(d["content"].split())
    out[slug] = {
        "content": d["content"],
        "wordCount": wc,
        "corrections": d["corrections"],
        "sourcesChecked": d["sourcesChecked"],
        "unverifiable": d["unverifiable"],
    }

with open("/home/hatch/workspace/global-defense-brief/hidden_files/audit/batch2.json", "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)

print("written:", len(out), "articles")
for slug, d in out.items():
    print(slug, d["wordCount"], "words")
