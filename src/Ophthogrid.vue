<template>
  <div id="app">
    <h1>Guide to Ophtho Medications</h1>
    <nav class="nav">
      <menu class="nav__controls">
        <svg class="nav__icon">
          <use xlink:href="#filter">
            <svg
              viewBox="0 0 24 24"
              id="filter"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1 0l9 15.094v5.906l4 3v-8.906l9-15.094h-22zm18.479 2l-2.981 5h-8.996l-2.981-5h14.958z"
              ></path>
            </svg>
          </use>
        </svg>
        <li
          v-for="(active, menu) in menus"
          class="nav__label"
          :class="{
            'nav__label--active': active,
            'nav__label--filter': activeFilters[menu].length,
          }"
          @click="setMenu(menu, active)"
          v-bind:key="menu"
        >
          {{ menu }}
        </li>
        <div class="name__filter">
          <label>Name:</label>
          <input type="text" v-model="drugSearch" />
        </div>
        <li class="nav__label nav__label--clear" @click="clearAllFilters">
          Clear all
        </li>
      </menu>
      <label class="nav__label" @click="modal = !modal">About this Guide</label>
    </nav>
    <transition-group
      name="dropdown"
      tag="section"
      class="dropdown"
      :style="dropdown"
    >
      <menu
        v-for="(options, filter) in filters"
        class="filters"
        v-show="menus[filter]"
        ref="menu"
        :key="filter"
      >
        <template>
          <li
            v-for="(active, option) in options"
            class="filters__item"
            :class="{ 'filters__item--active': active }"
            @click="setFilter(filter, option)"
            v-bind:key="option"
          >
            {{ option }}
          </li>
        </template>
      </menu>
    </transition-group>

    <div class="centered">
      <transition-group class="cards" name="cards">
        <article class="card" v-for="drug in filteredItems" :key="drug">
          <div class="card-content front-card">
            <h2>{{ drug.Name }}</h2>
            <h3>{{ drug.Class.split(",").join(", ") }}</h3>
            <hr />
            <a
              class="more-link"
              href="#"
              v-on:click.prevent="changeInfo(drug.Name)"
              >See more info</a
            ><br />
            <transition name="slide-left" mode="out-in">
              <div
                v-if="!infoDisplay[drug.Name]"
                key="`${drug.Name}_basic_info`"
              >
                <!--
                  Uses: {{ drug.Condition }}</br>
                  -->
                Typical Dose Range: {{ drug.Dose }}
                <mark-down :key="`${drug.Name}`">{{ drug.Notes }}</mark-down>
              </div>
              <div v-else key="`${drug.Name}_more_info`">
                Mechanism of action:
                <mark-down>{{ drug.MOA }}</mark-down> Warnings:
                <mark-down>{{ drug.Warnings }}</mark-down>
              </div>
            </transition>
          </div>
          <!-- .card-content -->
        </article>
        <!-- .card -->
      </transition-group>
      <!-- .cards -->
    </div>
    <div class="debug">
      <pre><code>DrugSearch: {{ drugSearch }}</code></pre>
      <pre><code>Filter Classes: {{ filters.classes }}</code></pre>
      <pre><code>Filter Cost: {{ filters.cost }}</code></pre>
      <pre><code>Active Filter Conditions: {{ activeFilters }}</code></pre>
      <pre><code>Info Display: {{ infoDisplay }}</code></pre>
    </div>

    <transition name="modal">
      <section v-if="modal" class="modal" @click="modal = false">
        <article class="modal__content" @click.stop>
          <h4 class="modal__title">
            Filter results by disease, drug class, cost, and name.
          </h4>

          <h5 class="" @click="modal = false">
            Designed and implemented by Thomas Chen DVM, MS, DACVO :)
          </h5>

          <button class="modal__close" @click="modal = false">&times;</button>
        </article>
      </section>
    </transition>
  </div>
</template>

<script>
var alldrugs = [
  {
    Name: "Gentamicin",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition: "Infected Ulcer",
    Dose: "BID (prophylaxis) - TID",
    Notes:
      "* Narrow spectrum antibiotic - Gram negative\n* Can be used for prophylaxis but since most infections are Gram positive, may not be best choice for empirical/prophylactic use\n* There is some concern for gentamicin inhibiting wound healing in cell culture - do not dose excessively\n* More appropriate for use if rods are noted on cytology or as indicated by culture. \n* Can be used in combination with a compounded topical beta-lactam (e.g. cephalosporin) for possible synergistic effect - do not combine together, give separately.\n",
    MOA:
      "* Aminoglycoside - inhibits bacterial protein synthesis at the 30S ribosome",
    Warnings:
      "* Subconjunctival injection of this antibiotic (with the injectable form) can result in systemic absorption. \n* Is toxic to intraocular structures (epitheliotoxic) and is used as chemical ablation agent in end-stage glaucoma",
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "Tobramycin",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition: "Infected Ulcer",
    Dose: "BID (prophylaxis) - TID",
    Notes:
      "* Narrow spectrum antibiotic - Gram negative\n* Can be used for prophylaxis but since most infections are Gram positive, may not be best choice for empirical/prophylactic use\n* There is conflicting evidence of tobramycin inhibiting wound healing in cell culture (like its cousin Gentamicin) - do not dose excessively\n* More appropriate for use if rods are noted on cytology or as indicated by culture. \n* Can be used in combination with a compounded topical beta-lactam (e.g. cephalosporin) for possible synergistic effect - do not combine together, give separately.\n",
    MOA:
      "* Aminoglycoside - inhibits bacterial protein synthesis at the 30S ribosome",
    Warnings:
      "* Subconjunctival injection of this antibiotic (with the injectable form) can result in systemic absorption",
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "NeoPolyGram",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition: "Simple corneal ulcer,Indolent ulcer",
    Dose: "BID (prophylaxis)",
    Notes:
      "* Broad spectrum combination (Neo: G-, Poly: G-, Gram: G+)\n* The author's preferred prophylactic topical since resistance is less likely with combination of drugs\n* Poor penetration through intact epithelium (so not a big deal in superficial ulcers but problematic if trying to treat a corneal abscess)",
    MOA:
      "* Neomycin - aminoglycoside inhibition of protein synthesis (30S)\n* Polymixin - detergent that disrupts cell membranes (not cell walls) - best against Gram negative\n* Gramicidin - detergent as well but targeted toward Gram positive",
    Warnings:
      "* There is a case series reporting anaphylaxis in 61 cats (over a period of 17 years) within 4 hours of exposure to topical antibiotics, all of which contained polymixin; this does not mean you shouldn't use this medication in cats as the reaction is very very rare, but only to dispense antibiotics judiciously (which really you should be doing anyway)",
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "NeoPolyBac",
    Formulations: "ophthalmic ointment",
    Class: "Topical Antibiotic",
    Condition: "Simple corneal ulcer,Indolent ulcer",
    Dose: "BID (prophylaxis)",
    Notes:
      "* Broad spectrum combination (Neo: G-, Poly: G-, Bac: G+)\n* The author's preferred prophylactic topical since resistance is less likely with combination of drugs\n* Poor penetration through intact epithelium (so not a big deal in superficial ulcers but problematic if trying to treat a corneal abscess)",
    MOA:
      "* Neomycin - aminoglycoside inhibition of protein synthesis (30S)\n* Polymixin - detergent that disrupts cell membranes (not cell walls) - best against Gram negative\n* Bacitracin - cell wall inhibitor, Gram positive spectrum",
    Warnings:
      "* There is a case series reporting anaphylaxis in 61 cats (over a period of 17 years) within 4 hours of exposure to topical antibiotics, all of which contained polymixin; this does not mean you shouldn't use this medication in cats as the reaction is very very rare, but only to dispense antibiotics judiciously (which really you should be doing anyway)",
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "NeoPolyDex",
    Formulations: "ophthalmic solution,ophthalmic ointment",
    Class: "Topical Antibiotic,Topical Steroid Anti-inflammatory",
    Condition:
      "Non-ulcerative Keratitis,Conjunctivitis,Eosinophilic keratitis,Keratoconjunctivitis sicca (KCS/Dry Eye),Uveitis,Hyphema,Pannus/Chronic superficial keratitis,Allergic conjunctivitis",
    Dose: "BID (mild-moderate) - QID (severe)",
    Notes:
      "* Antibiotic-steroid combination\n* Can be used for immune-mediated conditions (e.g. pannus, nodular granulomatous episcleritis) when steroid-alone drops are expensive or unavailable\n* Handy where a secondary bacterial infection is also present as well as keratoconjunctivitis such as in chronic dry eye\n* Can be used for moderate-severe cases of conjunctivitis",
    MOA:
      "* Neomycin - aminoglycoside inhibition of protein synthesis (30S)\n* Polymixin - detergent that disrupts cell membranes (not cell walls) - best against Gram negative\n* Dexamethasone - steroidal anti-inflammatory ",
    Warnings:
      "* Avoid use in most ulceratitive keratitis unless strongly suspected that the ulcer is secondary to immune-mediated causes (e.g. eosinophilic keratitis)\n* Caution in cats - many corneal/conjunctival disease is secondary to infection like herpes and steroid use may cause recrudescence \n* Avoid use in acute cases of dry eye as these eyes are prone to ulcerations (an import corollary to this is to always check tear production in a red eye lest you treat a dry eye with steroids and end up with a horrific ulcer)\n* There is a case series reporting anaphylaxis in 61 cats (over a period of 17 years) within 4 hours of exposure to topical antibiotics, all of which contained polymixin; this does not mean you shouldn't use this medication in cats as the reaction is very very rare, but only to dispense antibiotics judiciously (which really you should be doing anyway)",
    Cost: "$",
    Color: "Pink",
    CommonlyUsed: "Common",
  },
  {
    Name: "NeoPoly-Hydrocortisone",
    Formulations: "ophthalmic solution,ophthalmic ointment",
    Class: "Topical Antibiotic,Topical Steroid Anti-inflammatory",
    Condition: "Conjunctivitis,Allergic conjunctivitis",
    Dose: "BID",
    Notes:
      "* Antibiotic-steroid combination\n* Hydrocortisone is a very weak steroid so its efficacy in treating immune-mediate disease is slim to none\n* Useful for mild conjunctivitis but has limited efficacy otherwise, you're probably better off with NeoPolyDex",
    MOA:
      "* Neomycin - aminoglycoside inhibition of protein synthesis (30S)\n* Polymixin - detergent that disrupts cell membranes (not cell walls) - best against Gram negative\n* Hydrocortisone - weak steroidal anti-inflammatory",
    Warnings: "",
    Cost: "$",
    Color: "Pink",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Ciprofloxacin",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition:
      "Infected Ulcer,Corneal perforation,Melting corneal ulcer,Stromal ulcer",
    Dose: "BID-QID",
    Notes:
      "* Broad spectrum antibiotic - relatively good efficacy against Gram positive and negative organisms\n* 2nd generation fluoroquinolone\n* Has relatively good penetration into the cornea/eye but ofloxacin may be marginally better",
    MOA:
      "* 2nd generation fluoroquinolone (FQN)\n* Ok gram negative spectrum (gets better with latter generations in FQNs)\n* Good corneal penetration but less penetration than ofloxacin potentially (another 2nd gen FQN)\n* Inhibits bacterial DNA gyrase",
    Warnings:
      "* There are increased reports of resistance in human medicine - use judiciously in cases where infection is known or highly suspected or in high-risk patients",
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "Ofloxacin",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition: "Infected Ulcer,Corneal perforation,Melting corneal ulcer",
    Dose: "BID-QID",
    Notes:
      "* Broad spectrum antibiotic - relatively good efficacy against Gram positive and negative organisms\n* 2nd generation fluoroquinolone\n* Good corneal and intraocular penetration (probably up-to but not past the anterior chamber)\n* Usually well-tolerated",
    MOA:
      "* 2nd generation fluoroquinolone (FQN)\n* Ok gram negative spectrum (gets better with latter generations in FQNs)\n* Good corneal penetration\n* Inhibits bacterial DNA gyrase",
    Warnings:
      "* There are increased reports of resistance in human medicine - use judiciously in cases where infection is known or highly suspected or in high-risk patients",
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "Levofloxacin",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition: "Infected Ulcer,Corneal perforation,Melting corneal ulcer",
    Dose: "BID-QID",
    Notes:
      "* Broad spectrum antibiotic - relatively good efficacy against Gram positive and negative organisms\n* 2nd generation fluoroquinolone\n* Good corneal and intraocular penetration (probably up-to but not past the anterior chamber)",
    MOA:
      "* 3rd generation fluoroquinolone (greater G- spectrum compared to earlier generations",
    Warnings:
      "* Use in cases where sensitivities indicate its use (when everything else is resistant)\n* Should not be first-line empirical treatment",
    Cost: "$-$$",
    Color: "Tan",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Moxifloxacin",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition: "Infected Ulcer,Corneal perforation,Melting corneal ulcer",
    Dose: "BID-QID",
    Notes:
      "* Broad spectrum antibiotic - relatively good efficacy against Gram positive and negative organisms\n* 4th generation fluoroquinolone\n* Good corneal and intraocular penetration (probably up-to but not past the anterior chamber)",
    MOA: "* 4th generation fluoroquinolone",
    Warnings:
      "* Use in cases where sensitivities indicate its use (when everything else is resistant)\n* Should not be first-line empirical treatment",
    Cost: "$-$$",
    Color: "Tan",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Gatifloxacin",
    Formulations: "ophthalmic solution",
    Class: "Topical Antibiotic",
    Condition: "Infected Ulcer,Corneal perforation,Melting corneal ulcer",
    Dose: "BID-QID",
    Notes:
      "* Broad spectrum antibiotic - relatively good efficacy against Gram positive and negative organisms\n* 4th generation fluoroquinolone\n* Good corneal and intraocular penetration (probably up-to but not past the anterior chamber)",
    MOA: "* 4th generation fluoroquinolone",
    Warnings:
      "* Use in cases where sensitivities indicate its use (when everything else is resistant)\n* Should not be first-line empirical treatment",
    Cost: "$-$$",
    Color: "Tan",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Erythromicin",
    Formulations: "ophthalmic ointment",
    Class: "Topical Antibiotic",
    Condition: "Conjunctivitis,Simple corneal ulcer",
    Dose: "BID",
    Notes:
      "* Primarily for Gram positive but most often used against intracellular organisms - namely Chlamydia and Mycoplasma in cats\n* Bacteriostatic drug so is not first line therapy in cases with active infections unless indicated by culture and sensitivity",
    MOA: "* Macrolide antibiotic that binds to 50S subunit",
    Warnings: "",
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "Oxytetracycline + Polymixin B (Terramycin)",
    Formulations: "ophthalmic ointment",
    Class: "Topical Antibiotic",
    Condition: "Conjunctivitis,Indolent ulcer,Simple corneal ulcer",
    Dose: "BID-TID",
    Notes:
      "* Broad spectrum antibiotic but use is typically limited to intracellular infections (Chlamydia & Mycoplasma in cats)\n* Has been reported to be efficacious in healing of indolent ulcers (dogs) in conjunction with debridement (TID dosing frequency)\n",
    MOA:
      "* Interferes with bacterial 30S subunit (protein synthesis)\n* Tetracyclines in general have been noted to have other beneficial effects: anticollagenase, anti-apoptotic, anti-inflammatory, anti-oxidative; it should be noted that these effects vary depending on the specific form of tetracycline in question (e.g. doxycycline is a more potent inhibitor of MMPs than tetracycline or minocycline)",
    Warnings:
      '* While technically broad spectrum, efficacy against "typical" bacteria such as Staph, Strep, or Pseudomonas may be limited due to increasing resistance; therefore targeted use is usually toward rickettsial organisms or intracellular bacteria (Chlamydia/Mycoplasma) where resistance is less common',
    Cost: "$",
    Color: "Tan",
    CommonlyUsed: "Common",
  },
  {
    Name: "Chloramphenicol",
    Formulations: "ophthalmic ointment",
    Class: "Topical Antibiotic",
    Condition: "Infected Ulcer",
    Dose: "BID-TID",
    Notes:
      "* Has to be ordered from a compounding pharmacy (1% concentration)\n* Typically only used when indicated by a culture and sensitivity (i.e. resistance is noted to everything else except chloramphenicol)\n* It is broad spectrum and has been shown to be efficacious against most Gram positive and negative bacteria, as well as intracellular bacteria (Chlamydia, Mycoplasma, Rickettsial organisms)\n* Importantly, however, resistance has been noted in Pseudomonas (a rarer infection than Staph or Strep, but terrible when present)\n* Also used for treatment of corneal abscesses due to good penetration",
    MOA:
      "* Inhibits 50S bacterial ribosomal subunit\n* Relatively good penetration in an ointment form ",
    Warnings:
      "* Warn owners to use gloves when applying as very rarely people can develop a fatal aplastic anemia from exposure; risk is low but it would not be ideal to have a client die horribly after treating their animal",
    Cost: "$$",
    Color: "Tan",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Cidofovir",
    Formulations: "ophthalmic solution",
    Class: "Topical Antiviral",
    Condition: "Feline Herpes",
    Dose: "BID",
    Notes:
      "* Has to be ordered from a compounding pharmacy (usually at a 0.5% concentration)\n* Long intracellular half-life reduces the frequency of dosing in contrast to other topical anti-virals",
    MOA:
      "* Is a cytosine analogue\n* Replacement of cytosine with the active metabolite of cidofovir prevents DNA or RNA replication of the virus",
    Warnings:
      "* Can cause nasolacrimal punctal stenosis in people and rabbits but not reported in cats",
    Cost: "$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Idoxuridine",
    Formulations: "ophthalmic solution,ophthalmic ointment",
    Class: "Topical Antiviral",
    Condition: "Feline Herpes",
    Dose: "q4-6h",
    Notes:
      "* Has to be ordered from a compounding pharmacy (0.5-1%) solution or ophthalmic ointment\n* Anecdotally well tolerated by cats but needs to be given frequently",
    MOA:
      "* Is a thymidine analogue that works through competitive inhibition which prevents viral DNA replication",
    Warnings: "",
    Cost: "$$",
    Color: "",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Trifluridine",
    Formulations: "ophthalmic solution",
    Class: "Topical Antiviral",
    Condition: "Feline Herpes",
    Dose: "q4-6h",
    Notes:
      "* Commercially available but expensive\n* Has to be given frequently - 4-6 times per day",
    MOA:
      "* Is a thymidine analogue that works through competitive inhibition which prevents viral DNA replication",
    Warnings:
      "* Expensive and anecdotally may not be well tolerated by some cats",
    Cost: "$$$",
    Color: "",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Famciclovir",
    Formulations: "oral tablet",
    Class: "Oral Anti-Viral",
    Condition: "Feline Herpes",
    Dose: "90 mg/kg PO TID",
    Notes:
      "* For an average size 10 lb cat - works out to be about a 500 mg tablet orally three times daily\n* This is a very large tablet to try to give a cat, so generally the author will start with a 250 mg tablet (or half a 500) and if signs do not improve over a 2-4 week course, go to a higher dose or consider co-administration with cidofovir\n* Probably the most actively studied antiviral in cats",
    MOA:
      "* Is converted to a guanosine analog which competitively inhibits viral replication\n* A high dose is needed in cats due to limited availability of the enzymes required to convert famciclovir to its active form, penciclovir",
    Warnings:
      "* Side effects can occur (10/59 [17%] cats in one study) and are usually gastrointestinal (e.g. diarrhea or inappetence) and resolve after discontinuing ",
    Cost: "$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Natamycin",
    Formulations: "ophthalmic solution",
    Class: "Topical Anti-fungal",
    Condition: "Fungal keratitis",
    Dose: "q2h-BID",
    Notes:
      "* Only anti-fungal labeled for ocular use (5% ophthalmic suspension)\n* Good for filamentous fungi\n* Limited corneal penetration so efficacy in fungal corneal abscesses may be limited",
    MOA:
      "* Polyene - binds to ergosterol in fungal cell membranes to form complexes that result in leakage from the fungal cell",
    Warnings:
      "* Fairly safe medication but not for wallets\n* Viscosity may make injection through an SPL harder than other solutions",
    Cost: "$$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Amphotericin B",
    Formulations: "ophthalmic solution",
    Class: "Topical Anti-fungal",
    Condition: "Fungal keratitis",
    Dose: "q2h-6h topically, q48h x 3 doses (subconj)",
    Notes:
      "* Broad spectrum anti-fungal but no specific topical formulation\n* Good against yeast and filamentous fungi\n* Can reconstitute (use sterile water not saline) solution into a 0.15% form (can do higher concentrations but can be irritating) for topical use \n* If you do create this form, protect from light and keep it in the fridge and it will be good for at least 7 days\n* Can be used topically (usually through an SPL) or injected subconjunctivally or with proper expertise, injected intrastromally\n* Is thick and viscous so may accumulate in deeper ulcers prolonging contact time; ",
    MOA:
      "* Polyene - binds to ergosterol in fungal cell membranes to form complexes that result in leakage from the fungal cell",
    Warnings:
      "* Anecdotally can induce a fair amount of local irritation/inflammation when given subconjunctivally\n* Concentrations above 0.3% reported to be irritating (in literature, reports of going up as high as 3% though)",
    Cost: "$$-$$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Miconazole ",
    Formulations: "ophthalmic solution",
    Class: "Topical Anti-fungal",
    Condition: "Fungal keratitis",
    Dose: "q2h-BID",
    Notes:
      "* Can either be compounded into a 1% ophthalmic solution or can utilize (obviously off-label) 2% vaginal cream\n* Variable efficacy reported in the literature for Aspergillus and Fusarium in vitro",
    MOA: "* Azole - fungistatic, inhibits ergosterol synthesis",
    Warnings:
      "* In lab culture, has been shown to slow or alter keratocyte growth",
    Cost: "$-$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Silver sulfadiazine",
    Formulations: "topical ointment,injectable",
    Class: "Topical Anti-fungal",
    Condition: "Fungal keratitis",
    Dose: "q2h (in beginning)-BID",
    Notes:
      '* Technically broad spectrum against bacteria and fungi usually used for skin application but is safe for cornea and conjunctival use as well\n* Recent study showed good efficacy in vitro against fungal isolates seen in horses\n* Clearly states on the packaging "NOT FOR OPHTHALMIC USE" so definitely off-label; recommend obtaining consent for use and potentially avoiding in cases where lawyers could be involved\n* Main benefit is cost; could be beneficial in early cases of keratitis or infection',
    MOA:
      "* No one is really sure how/why the SSD works although silver is biocidal with a wide range of effects on cellular metabolism",
    Warnings:
      "* Can cause bluish change to skin/sclera (discontinue if seen) and be irritating\n* Do not put in SPL\n* Does not need to be refrigerated",
    Cost: "$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Voriconazole",
    Formulations: "ophthalmic solution",
    Class: "Topical Anti-fungal",
    Condition: "Fungal keratitis",
    Dose: "q2-4h",
    Notes:
      "* No commercial eye product, usually reconstituted from the IV form - 19 mL of sterile water in 200 mg vial to create 1% solution, refrigerate and discard after 1 month\n* Oral use has good bioavailability however dosing in horses is usually cost prohibitive\n* In vitro study found to be more effective in southern and midwestern US than some other antifungals",
    MOA:
      "* Azole - inhibits ergosterol synthesis which effect cell membrane synthesis",
    Warnings:
      "* Most adverse effects are reported in people and not horses - include dermatologic reactions or photosensitivity of the skin",
    Cost: "Jeff Bezos",
    Color: "",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Cyclosporine",
    Formulations: "ophthalmic solution",
    Class: "Topical Immune-modulatory,Topical Lacromimetic ",
    Condition:
      "Keratoconjunctivitis sicca (KCS/Dry Eye),Non-ulcerative Keratitis,Eosinophilic keratitis",
    Dose: "q6-24h",
    Notes:
      "* The active ingredient in optimmune which is a 0.2% concentration of it\n* Commonly compounded into 1-2% formulations which are handy for more severe cases\n* Used primarily for treatment of KCS (immune-mediated lacrimal adenitis) but is also used for immune-mediated keratitis (sometimes as a monotherapy, sometimes in conjunction with topical steroids)\n* Dosing for KCS is usually BID-TID initially, for immune mediated disease may be more frequent depending on severity",
    MOA:
      "* Complicated mechanism of action that ultimately results in the prevention of transcription for IL-2, a T-Cell interleukin\n* Inhibition results in less IL-2 with less T-cell activation",
    Warnings:
      "* Does not penetrate well through intact epithelium (so topical use for uveitis is not indicated)\n* Control of significant keratitis might require use of steroids initially\n* If compounded, is usually placed in a lipid vehicle to which some animals may be sensitive to, can try switching vehicles if this is suspected",
    Cost: "$-$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Tacrolimus",
    Formulations: "ophthalmic solution",
    Class: "Topical Immune-modulatory,Topical Lacromimetic ",
    Condition:
      "Keratoconjunctivitis sicca (KCS/Dry Eye),Non-ulcerative Keratitis,Eosinophilic keratitis",
    Dose: "q6-24h",
    Notes:
      "* Similar to cyclosporine in the indications for use\n* No commercial product so has to be compounded in a 0.01-0.03% solution (lesser concentration compared to Cyclosporine is due to increased potency)\n* Used primarily for treatment of KCS (immune-mediated lacrimal adenitis) but is also used for immune-mediated keratitis (sometimes as a monotherapy, sometimes in conjunction with topical steroids)\n* Dosing for KCS is usually BID-TID initially, for immune mediated disease may be more frequent depending on severity",
    MOA:
      "* Complicated mechanism of action that ultimately results in the prevention of transcription for IL-2, a T-Cell interleukin (in a different manner to cyclosporine but similar effects)\n* Inhibition results in less IL-2 with less T-cell activation",
    Warnings:
      "* Does not penetrate well through intact epithelium (so topical use for uveitis is not indicated)\n* Control of significant keratitis might require use of steroids initially\n* If compounded, is usually placed in a lipid vehicle to which some animals may be sensitive to, can try switching vehicles if this is suspected\n* Can also be compounded into an aqueous (not lipid) formula which may be better tolerated ",
    Cost: "$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Pimecrolimus",
    Formulations: "ophthalmic solution",
    Class: "Topical Immune-modulatory,Topical Lacromimetic ",
    Condition:
      "Keratoconjunctivitis sicca (KCS/Dry Eye),Non-ulcerative Keratitis,Eosinophilic keratitis",
    Dose: "q6-24h",
    Notes:
      "* Pronounced \"pee-mek-rowe-li-mus\"\n* Similar to cyclosporine/tacro in the indications for use\n* No commercial product so has to be compounded in a 1% solution\n* Used primarily for treatment of KCS (immune-mediated lacrimal adenitis) but also has evidence of effective in cases of pannus as well\n* Dosing is usually BID\n* Isn't broadly used because it's newer and not many compounding pharmacies carry it but could be an option if cyclosporine/tacrolimus not well tolerated",
    MOA:
      "* Complicated mechanism of action that ultimately results in the prevention of transcription for IL-2, a T-Cell interleukin (in a similar manner to tacrolimus)\n* Inhibition results in less IL-2 with less T-cell activation",
    Warnings:
      "* Does not penetrate well through intact epithelium (so topical use for uveitis is not indicated)\n* Control of significant keratitis might require use of steroids initially\n* If compounded, is usually placed in a lipid vehicle to which some animals may be sensitive to, can try switching vehicles if this is suspected",
    Cost: "$$",
    Color: "",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Serum",
    Formulations: "biologic product",
    Class: "Anti-collagenase",
    Condition:
      "Infected Ulcer,Melting corneal ulcer,Fungal keratitis,Stromal ulcer",
    Dose: "q2-12h",
    Notes:
      '* Serum or plasma is used for its anti-collagenase components (macrogloblins)\n* The main indication is to reduce or stop enzymatic degradation of the cornea (melting or stromal loss) from endogenous or exogenous matrix metalloproteinases (MMPs) \n* Frequency depends on severity of melting or stromal loss - if aggressive do q1-2 hours acutely and then taper as condition stabilizes\n* Can be made from an animal\'s own blood (draw, spin down, place in syringes) or can used "banked" serum from other animals or banked commercial plasma; can also use serum from another species - e.g. horse serum on dogs\n* Freeze for storage and then thaw and place in fridge with active use',
    MOA:
      "* Contains alpha2-macroglobulins that will bind and inactivate collagenases\n* Serum also contains other beneficial compounds (growth factors, etc.) but the effect of these factors on corneal wound healing is limited in the veterinary literature and probably fall into the \"can't hurt might help\" category when used with ulcers that don't have a major collagenase component",
    Warnings:
      "* Keep frozen when not in use (can bank in clinic)\n* Discard after prolonged storage - just how long they can be kept is unknown; a study looking at efficacy of frozen serum found no decrease in efficacy for up to 6 months",
    Cost: "$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "EDTA",
    Formulations: "ophthalmic solution,ophthalmic ointment",
    Class: "Chelator,Anti-collagenase",
    Condition: "Calcific corneal degeneration,Melting corneal ulcer",
    Dose: "q6-24h",
    Notes:
      "* No commercial eye product so has to be compounded into a 0.2-2% solution or ointment\n* Mostly used for calcific keratopathy or degeneration and potentially for melting ulcers",
    MOA:
      "* Chelates Ca2+ and Zn2+, cofactors for collagenase activity thereby preventing activation of those enzymes",
    Warnings:
      "* Higher concentrations can be irritating to the eye so usually the author will do up to a 1% topically when applying at home; some dogs may still not like it so warn owners to watch carefully after application and stop any rubbing after giving",
    Cost: "$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Ketorolac 0.4%, 0.5%",
    Formulations: "ophthalmic solution",
    Class: "Topical Non-steroidal Anti-inflammatory (NSAID)",
    Condition: "Uveitis,Allergic conjunctivitis",
    Dose: "q6-24h",
    Notes:
      "* Indicated for control of mild-moderate uveitis but has been show in off-label studies in people to be beneficial for allergic conjunctivitis at a QID dosing (this is in people but can try for dogs)\n* Indicated for control of mild-moderate uveitis\n* Few direct comparisons of topical NSAIDs in the veterinary world have been performed (gluts of research in people in contrast); varying methods and concentrations make direct comparisons difficult\n* To the author's knowledge, little to no studies on clinical efficacy in veterinary patients for the topical form of ketorolac",
    MOA:
      "* Nonspecific COX1 and COX2 inhibitor with resultant prostaglandin inhibition (and all the good/bad things associated with it)",
    Warnings:
      "* Topical NSAIDS can result in ulcers in some patients as well as delay corneal wound healing (shown in vitro)\n* While it's unclear how much topical NSAIDS contribute to ulceration or slowing down of healing, the author will avoid use of topical NSAIDS in ulcerative keratitis and halt its usage with ulceration\n* Per the drug insert, ketorolac may affect thrombocyte aggregation which may cause increased bleeding; potentially avoid use in hyphema cases",
    Cost: "$-$$",
    Color: "Gray",
    CommonlyUsed: "Common",
  },
  {
    Name: "Flurbiprofen 0.03%",
    Formulations: "ophthalmic solution",
    Class: "Topical Non-steroidal Anti-inflammatory (NSAID)",
    Condition: "Uveitis",
    Dose: "q6-24h",
    Notes:
      "* Indicated for control of mild-moderate uveitis\n* Few direct comparisons of topical NSAIDs in the veterinary world have been performed (gluts of research in people in contrast); varying methods and concentrations make direct comparisons difficult\n* In cats, one study suggested diclofenac was the better NSAID compared to flurbiprofen \n* In dogs, there have been a number of studies from the late 1990s that have shown efficacy for controlling uveitis but how these compare to newer NSAIDs is less clear",
    MOA:
      "* Nonspecific COX1 and COX2 inhibitor with resultant prostaglandin inhibition (and all the good/bad things associated with it)",
    Warnings:
      "* Topical NSAIDS can result in ulcers in some patients as well as delay corneal wound healing (shown in vitro)\n* While it's unclear how much topical NSAIDS contribute to ulceration or slowing down of healing, the author will avoid use of topical NSAIDS in ulcerative keratitis and halt its usage with ulceration\n* One study in cats showed increased IOP with use of flurbiprofen compared to control (so be mindful of use if ocular hypertension is a comorbidity)",
    Cost: "$-$$",
    Color: "Gray",
    CommonlyUsed: "Common",
  },
  {
    Name: "Diclofenac 0.3%",
    Formulations: "ophthalmic solution",
    Class: "Topical Non-steroidal Anti-inflammatory (NSAID)",
    Condition: "Uveitis",
    Dose: "q6-24h",
    Notes:
      "* Indicated for control of mild-moderate uveitis\n* Few direct comparisons of topical NSAIDs in the veterinary world have been performed (gluts of research in people in contrast); varying methods and concentrations make direct comparisons difficult\n* In cats, one study suggested diclofenac was the better NSAID compared to flurbiprofen \n* In dogs, a similar findings were noted in 1 study but the difference was small and a 1% solution was used (commercially a 0.3% solution is available).",
    MOA:
      "* Nonspecific COX1 and COX2 inhibitor with resultant prostaglandin inhibition (and all the good/bad things associated with it)",
    Warnings:
      "* Topical NSAIDS can result in ulcers in some patients as well as delay corneal wound healing (shown in vitro)\n* While it's unclear how much topical NSAIDS contribute to ulceration or slowing down of healing, the author will avoid use of topical NSAIDS in ulcerative keratitis and halt its usage with ulceration\n* One study in cats showed increased IOP with use of diclofenac compared to control (so be mindful of use if ocular hypertension is a comorbidity)",
    Cost: "$-$$",
    Color: "Gray",
    CommonlyUsed: "Common",
  },
  {
    Name: "Bromfenac 0.9%",
    Formulations: "ophthalmic solution",
    Class: "Topical Non-steroidal Anti-inflammatory (NSAID)",
    Condition: "Uveitis",
    Dose: "q6-24h",
    Notes:
      "* Indicated for control of mild-moderate uveitis\n* Few direct comparisons of topical NSAIDs in the veterinary world have been performed (gluts of research in people in contrast); varying methods and concentrations make direct comparisons difficult\n* Has been studied in dogs in the context of post-cataract surgery pressures and inflammation which showed potential risk of increased IOP post-phaco; anti-inflammatory effects comparable with prednisolone acetate 1 week+ post-operatively (immediately after seemed to have less control of post-op uveitis)",
    MOA:
      "* Bromfenac is unique in that it's more COX2 specific compared to its other topical NSAID friends\n* Has good penetrance through cornea into intraocular tissues",
    Warnings:
      "* Topical NSAIDS can result in ulcers in some patients as well as delay corneal wound healing (shown in vitro)\n* While it's unclear how much topical NSAIDS contribute to ulceration or slowing down of healing, the author will avoid use of topical NSAIDS in ulcerative keratitis and halt its usage with ulceration\n* One study in cats showed increased IOP with use of diclofenac compared to control (so be mindful of use if ocular hypertension is a comorbidity)",
    Cost: "$$",
    Color: "Gray",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Nepafenac 0.1%",
    Formulations: "ophthalmic solution",
    Class: "Topical Non-steroidal Anti-inflammatory (NSAID)",
    Condition: "Uveitis",
    Dose: "q8h",
    Notes:
      "* Indicated for control of mild-moderate uveitis\n* No studies on efficacy in veterinary patients",
    MOA:
      "* Nepfanac is only pro-drug NSAID availalbe - is converted to active form (amfenac) by ocular tissues which then exerts anti-inflammatory function (COX1 & COX2 inhibition)",
    Warnings:
      "* Topical NSAIDS can result in ulcers in some patients as well as delay corneal wound healing (shown in vitro)\n* While it's unclear how much topical NSAIDS contribute to ulceration or slowing down of healing, the author will avoid use of topical NSAIDS in ulcerative keratitis and halt its usage with ulceration\n* One study in cats showed increased IOP with use of diclofenac compared to control (so be mindful of use if ocular hypertension is a comorbidity)\n* Nepafenac is stupid expensive",
    Cost: "Jeff Bezos",
    Color: "Gray",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Prednisolone acetate 1%",
    Formulations: "ophthalmic solution",
    Class: "Topical Steroid Anti-inflammatory",
    Condition: "Uveitis,Conjunctivitis,Non-ulcerative Keratitis",
    Dose: "q6-24h",
    Notes:
      "* A commonly used topical corticosteroid for inflammatory diseases of the eye\n* Penetration with the acetate formulation is superior compared to other corticosteroids; particularly useful for anterior uveitis\n* Has a relative strength of 4 compared to hydrocortisone (1) and dexamethasone (25) \n* Dosing is typically based on severity of disease with regular monitoring to assess response",
    MOA:
      "* Broad and significant effects on transcription of anti-inflammatory or pro-inflammatory genes as well as direct affects on cell mediators and receptors\n* Indirectly inhibits arachidonic acid pathway ",
    Warnings:
      "* Contraindicated in cases of corneal ulceration in veterinary patients or in cases where active infection (viral, bacterial, fungal) is present\n* Can cause a reversible increase in IOP in some patients/species; altered dosing is indicated if IOP increases are significant",
    Cost: "$-$$",
    Color: "Pink",
    CommonlyUsed: "Common",
  },
  {
    Name: "Dexamethasone 0.1%",
    Formulations: "ophthalmic solution",
    Class: "Topical Steroid Anti-inflammatory",
    Condition: "Uveitis,Conjunctivitis,Non-ulcerative Keratitis",
    Dose: "q6-24h",
    Notes:
      "* A commonly used topical corticosteroid for inflammatory diseases of the eye\n* While more potent compared to prednisolone acetate, penetrance into the eye is less (especially for the phosphate formulations); can still be used for anterior uveitis however if response is incomplete or partial consider switching to prednisolone acetate\n* Has a relative strength of 25 compared to hydrocortisone (1) and prednisolone acetate (4) \n* Dosing is typically based on severity of disease with regular monitoring to assess response\n* Can be packaged up with Tobramycin (Tobradex) or Neomycin/Polymixin; stand-alone use is recommended in animals with sensitivity to topical antibiotics (e.g. cats)",
    MOA:
      "* Broad and significant effects on transcription of (up-regulation) anti-inflammatory or (down-regulation) pro-inflammatory genes as well as direct affects on cell mediators and receptors\n* Indirectly inhibits arachidonic acid pathway ",
    Warnings:
      "* Contraindicated in cases of corneal ulceration in veterinary patients or in cases where active infection (viral, bacterial, fungal) is present\n* Can cause a reversible increase in IOP in some patients/species; altered dosing is indicated if IOP increases are significant",
    Cost: "$-$$",
    Color: "Pink",
    CommonlyUsed: "Common",
  },
  {
    Name: "Dorzolamide 2%",
    Formulations: "ophthalmic solution",
    Class: "Topical Glaucoma/Ocular hypotensives",
    Condition: "Primary Glaucoma,Secondary Glaucoma",
    Dose: "TID",
    Notes:
      '* Safe for use in both primary and secondary glaucomas\n* Trade name is "Trusopt"\n* Can be used alone or bundled up with Timolol as one drug (Cosopt) in which case dosing is BID (vs TID)',
    MOA:
      "* Carbonic anhydrase inhibitor (CAI)\n* Carbonic anhydrase is an enzyme that catalyzes conversion of water to bicarb (HCO3-) and hydrogen ions (H+)\n* Inhibition of this process leads to lowered concentrations bicarb that then lower sodium and water outflow (aqueous humor production)",
    Warnings:
      "* Can sting after applications due to viscosity and acidity\n* Idiosyncratic keratitis has been reported in patients on long-term use with dorzolamide (median time in report was about a year of continued use)\n* Dogs with the CAI reaction exhibit marked ulcerative/non-ulcerative corneal neovascularization that was poorly responsive to topical anti-inflammatories\n* Clinical signs improved within a few days after halting administration of CAI",
    Cost: "$-$$",
    Color: "Orange",
    CommonlyUsed: "Common",
  },
  {
    Name: "Brinzolamide 1%",
    Formulations: "ophthalmic solution",
    Class: "Topical Glaucoma/Ocular hypotensives",
    Condition: "Primary Glaucoma,Secondary Glaucoma",
    Dose: "TID",
    Notes:
      '* Safe for use in both primary and secondary glaucomas\n* Trade name is "Azopt"\n* Is potentially better tolerated than Dorzolamide because it\'s less acidic\n* But poorly studied in veterinary medicine so comparative effect vs dorzolamide is unknown\n* Very expensive',
    MOA:
      "* Carbonic anhydrase inhibitor (CAI)\n* Carbonic anhydrase is an enzyme that catalyzes conversion of water to bicarb (HCO3-) and hydrogen ions (H+)\n* Inhibition of this process leads to lowered concentrations bicarb that then lower sodium and water outflow (***lowers aqueous humor production***)",
    Warnings:
      "* Idiosyncratic keratitis has been reported in patients on long-term use with dorzolamide (median time in report was about a year of continued use)\n* Dogs with the CAI reaction exhibit marked ulcerative/non-ulcerative corneal neovascularization that was poorly responsive to topical anti-inflammatories\n* Clinical signs improved within a few days after halting administration of CAI",
    Cost: "$$$",
    Color: "Orange",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Timolol 0.5%",
    Formulations: "ophthalmic solution",
    Class: "Topical Glaucoma/Ocular hypotensives",
    Condition: "Primary Glaucoma,Secondary Glaucoma",
    Dose: "BID",
    Notes:
      '* Comes in a 0.25% solution but has minimal IOP lowering effect in animals, so use 0.5% solution which has a small effect on IOP but can be used for mild cases of ocular hypertension\n* Non-selective beta-blocker so use caution in cases of asthma or in patients with cardiac disease\n* Combination form with Dorzolamide is also commonly used; trade-named "Cosopt" which is easier to say (generics are widely used but it\'s usually easier to say "Ko-sopt" rather than the full name',
    MOA:
      "* Non-selective beta blocker\n* Precise mechanism is unknown but suspected to involve cAMP",
    Warnings:
      "* Mild systemic absorption is possible and since it's a nonselective beta blocker, it is possible for asthmatic animals to have greater susceptibility to attacks\n* Be wary of use in animals with cardiac disease as it has been shown to reduce heart rate (not clinically significant) in normal animals",
    Cost: "$",
    Color: "Yellow",
    CommonlyUsed: "Common",
  },
  {
    Name: "Latanoprost  0.005%",
    Formulations: "ophthalmic solution",
    Class: "Topical Glaucoma/Ocular hypotensives,Miotic",
    Condition: "Primary Glaucoma,Posterior Lens Luxation",
    Dose: "BID",
    Notes:
      '* Most valuable for treatment of primary glaucoma (less so for secondary)\n* Can also be used specifically as a miotic agent for posterior lens luxations\n* Can be used in an "acute" glaucoma spikes in place of mannitol; multiple doses can be given with reasonable time period (30-60 min) while monitoring IOP; usually works within 1-2 hours post-administration (again confirm that case is a primary glaucoma)',
    MOA:
      "* Prostaglandin analogue\n* In essence, mimics inflammation which increases unconventional outflow of aqueous humor and decreases production\n* Potent miosis in veterinary species due to binding of prostaglandin receptors in iris sphincter m. --> use contraindicated in secondary glaucoma from uveitis; can easily predispose to worsening glaucoma from with pupillary block",
    Warnings:
      "* Avoid use where posterior synechia or pupillary block glaucoma (anterior lens luxation) is a high risk \n* Comes in a tiny bottle (2.5 mL) which can run out quickly and frustrate owners or worse, cause them to stop and then not refill; caution owners and script out more bottles if necessary to prevent interruptions in therapy",
    Cost: "$-$$",
    Color: "Teal",
    CommonlyUsed: "Common",
  },
  {
    Name: "Travaprost 0.004%",
    Formulations: "ophthalmic solution",
    Class: "Topical Glaucoma/Ocular hypotensives,Miotic",
    Condition: "Primary Glaucoma,Posterior Lens Luxation",
    Dose: "BID",
    Notes:
      '* Essentially equivalent to latanoprost but more expensive\n* Most valuable for treatment of primary glaucoma (less so for secondary)\n* Can also be used specifically as a miotic agent for posterior lens luxations\n* Can be used in an "acute" glaucoma spikes in place of mannitol; multiple doses can be given with reasonable time period (30-60 min) while monitoring IOP; usually works within 1-2 hours post-administration (again confirm that case is a primary glaucoma)',
    MOA:
      "* Prostaglandin analogue\n* In essence, mimics inflammation which increases unconventional outflow of aqueous humor and decreases production\n* Potent miosis in veterinary species due to binding of prostaglandin receptors in iris sphincter m. --> use contraindicated in secondary glaucoma from uveitis; can easily predispose to worsening glaucoma from with pupillary block",
    Warnings:
      "* Avoid use where posterior synechia or pupillary block glaucoma (anterior lens luxation) is a high risk \n* Comes in a tiny bottle (2.5 mL) which can run out quickly and frustrate owners or worse, cause them to stop and then not refill; caution owners and script out more bottles if necessary to prevent interruptions in therapy",
    Cost: "$$-$$$",
    Color: "Teal",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Bimatoprost 0.03%",
    Formulations: "ophthalmic solution",
    Class: "Topical Glaucoma/Ocular hypotensives,Miotic",
    Condition: "Primary Glaucoma,Posterior Lens Luxation",
    Dose: "BID",
    Notes:
      '* Used by ophthalmologist as an anecdotal "rescue" drug when maximum glaucoma therapy is not sufficient to keep IOP controlled (see MOA for differences in biochemistry)\n* Most valuable for treatment of primary glaucoma (less so for secondary)\n* Can also be used specifically as a miotic agent for posterior lens luxations\n* Can be used in an "acute" glaucoma spikes in place of mannitol; multiple doses can be given with reasonable time period (30-60 min) while monitoring IOP; usually works within 1-2 hours post-administration (again confirm that case is a primary glaucoma)',
    MOA:
      "* Prostaglandin analogue\n* In essence, mimics inflammation which increases unconventional outflow of aqueous humor and decreases production\n* Bimatoprost is unique among prostaglandin analogues because it does not have to be enzymatically converted to an active form like latanoprost - thus is postulated to work better \n* Potent miosis in veterinary species due to binding of prostaglandin receptors in iris sphincter m. --> use contraindicated in secondary glaucoma from uveitis; can easily predispose to worsening glaucoma from with pupillary block",
    Warnings:
      "* Avoid use where posterior synechia or pupillary block glaucoma (anterior lens luxation) is a high risk \n* Comes in a tiny bottle (2.5 mL) which can run out quickly and frustrate owners or worse, cause them to stop and then not refill; caution owners and script out more bottles if necessary to prevent interruptions in therapy",
    Cost: "$$-$$$",
    Color: "Teal",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Dorzolamide/Timolol",
    Formulations: "ophthalmic solution",
    Class: "Topical Glaucoma/Ocular hypotensives",
    Condition:
      "Primary Glaucoma,Secondary Glaucoma,Anterior lens luxation,Posterior Lens Luxation",
    Dose: "BID-TID",
    Notes:
      '* Combination of two glaucoma medications into one drop\n* Safe for use in both primary and secondary glaucomas\n* Commonly referred to by its trade name "Cosopt" (pronounced KO-sopt)\n* When given together, dosing of the Dorzolamide (usually TID) can be reduced to a BID dosing schedule\n* Comes out as a very viscous and thick eyedrop\n* Can sometimes be topically irritating (especially if there\'s an ulcer present)',
    MOA:
      "* Dorzolamide : Carbonic anhydrase inhibitor (CAI)\n** Carbonic anhydrase is an enzyme that catalyzes conversion of water to bicarb (HCO3-) and hydrogen ions (H+)\n* Inhibition of this process leads to lowered concentrations bicarb that then lower sodium and water outflow (aqueous humor production)\n* Timolol: Non-selective beta blocker\n** Precise mechanism is unknown but suspected to involve cAMP",
    Warnings:
      "* Most side effects probably originate from the Dorzolamide\n* Can sting after applications due to viscosity and acidity\n* Idiosyncratic keratitis has been reported in patients on long-term use with dorzolamide (median time in report was about a year of continued use)\n* Dogs with the CAI reaction exhibit marked ulcerative/non-ulcerative corneal neovascularization that was poorly responsive to topical anti-inflammatories\n* Clinical signs improved within a few days after halting administration of CAI",
    Cost: "$-$$",
    Color: "DarkBlue",
    CommonlyUsed: "Common",
  },
  {
    Name: "5% Sodium Chloride",
    Formulations: "ophthalmic solution",
    Class: "Hyperosmotics",
    Condition: "Endothelial Dystrophy/Degeneratoion,Bullous keratopathy",
    Dose: "q6-24h",
    Notes:
      "* Essentially concentrated saline ointment\n* Used for treatment of bullous keratopathy and endothelial degeneration/dystrophy\n* Can also be used in some cases of persistent ulcers where bulla formation is a concern",
    MOA:
      "* Osmotically draws fluid from corneal stroma hopefully reducing bulla formation\n* Will __not__ be sufficient to clear up corneal edema (set owner's expectations accordingly)",
    Warnings:
      "* Can sting after application\n* If poorly tolerated, reduce frequency/dose\n* Ointment is preferred over solution given longer residence time on corneal surface",
    Cost: "$-$$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Atropine 1%",
    Formulations: "ophthalmic solution,ophthalmic ointment",
    Class: "Mydriatic",
    Condition:
      "Uveitis,Simple corneal ulcer,Melting corneal ulcer,Infected Ulcer,Indolent ulcer,Stromal ulcer",
    Dose: "q12-48h",
    Notes:
      "* Cycloplegic for pain from ciliary body spasm that can occur from uveitis or ulcerative keratitis\n* Mydriasis is handy for use in uveitis as prevention of miosis is useful to prevent secondary glaucoma from posterior synechiae and helps improve vision if miosis is otherwise severe (especially in horses)\n* In an uninflamed eye, effect can last for 5-6 days in dogs and cats and potentially weeks in horses\n* The author will usually dose SID, BID, to EOD depending on degree of uveitis, pain",
    MOA:
      "* Nonselective anticholinergic (parasympatholytic)\n* Blocks receptors at smooth muscle",
    Warnings:
      "* Aggressive use is discouraged in cases of dry eye or if secondary glaucoma is a concern\n* Parasympatholytic activity reduces tear production\n* Cycloplegia can affect the iridocorneal angle and cause increases in IOP\n* Hypersalivation can be noted if medication is licked from nose (after traveling through nasolacrimal duct) or if travels to mouth, anecdotally ointments may lessen this effect",
    Cost: "$-$$",
    Color: "Red",
    CommonlyUsed: "Common",
  },
  {
    Name: "Tropicamide 1%",
    Formulations: "ophthalmic solution",
    Class: "Mydriatic",
    Condition: "Uveitis,Diagnostic agent",
    Dose: "once, q6-12h",
    Notes:
      '*  A "weaker" mydriatic which is most often used for dilated fundic exam but can also be used more frequently for dilation and to keep the pupil moving with uveitis\n* Mydriasis usually occurs within 15-30 min and effects last for a few hours post-dilation',
    MOA:
      "* Nonselective anticholinergic (parasympatholytic)\n* Blocks receptors at smooth muscle",
    Warnings:
      "* Relatively well tolerated especially if given just for diagnostic purposes",
    Cost: "$-$$",
    Color: "Red",
    CommonlyUsed: "Common",
  },
  {
    Name: "Phenylephrine 1%, 2.5%",
    Formulations: "ophthalmic solution",
    Class: "Mydriatic",
    Condition: "Horner's syndrome,Diagnostic agent",
    Dose: "once",
    Notes:
      "* Primarily used as a diagnostic agent to confirm Horner's syndrome\n* To assess for denervation hypersensitivity - place a drop in both eyes and observe for improvement in clinical signs (ptosis, enophthalmia) within 15-60 minutes\n* More detailed guidelines with regards to concentration and timeframe to expected response that correlate with first, second, third order lesions exist but are beyond the scope of this site\n* Expect blanching of conjunctiva with use",
    MOA:
      "* Direct acting sympathomimetic\n* In absence of sympathetic innervation (Horner's) receptors are up-regulated leading to a stronger reaction to exogenous sympathetic drugs",
    Warnings: "* Relatively well tolerated",
    Cost: "$$-$$$",
    Color: "Red",
    CommonlyUsed: "Uncommon",
  },
  {
    Name: "Fluorescein",
    Formulations: "ophthalmic solution",
    Class: "Diagnostic dye",
    Condition: "Diagnostic agent",
    Dose: "once",
    Notes:
      "* Ubiquitous use for diagnosis of a corneal ulcer\n* Also used to test for tear film quality: __tear film break up time [TBUT]__\n* Also used to test for nasolacrimal abnormalities: __Jones Test__, positive if stain noted at nostril\n* Also used to test for aqueous leakage: __Seidel Test__; strip of stain is painted over area, if green rivulet is noted, positive Seidel, consistent with aqueous leakage/perforation",
    MOA:
      "* Stain is hydrophilic, will bind to hydrophilic tissue (corneal stroma) but not to hydrophobic tissue (epithelium, Descemet's membrane)",
    Warnings:
      "* Can be irritating if applied in concentrated form to the cornea (e.g. applying strip directly to cornea)\n* Dilute with saline and place drop in eye or touch to conjunctiva",
    Cost: "$",
    Color: "",
    CommonlyUsed: "Common",
  },
  {
    Name: "Proparacaine 0.5%",
    Formulations: "ophthalmic solution",
    Class: "Topical Anesthetic",
    Condition: "Diagnostic agent",
    Dose: "once",
    Notes:
      "* Used as rapid-acting topical anesthetic to the cornea/conjunctiva\n* One drop is sufficient to obtain local analgesia for 10-15 minutes; a 2005 study showed greater effect and longer duration (30min) with 2 drops given 1 minute apart\n* Recommend to be stored refrigerated as efficacy wanes over time after 2 weeks of storage at room temperature\n* In cats, reported maximal effect is quite short at 5 minutes compared to other species",
    MOA:
      "* Sodium channel blocker - affects propagation of signaling through nerves",
    Warnings:
      '* Short duration of action in cats\n* Is less likely to cause topical irritation compared to tetracaine and lidocaine but still possible\n* Not appropriate for routine analgesia "at-home" treatment (effects are too short lived, rapid tachyphylaxis, and delayed wound healing with repeated use)',
    Cost: "$$",
    Color: "",
    CommonlyUsed: "Common",
  },
];

export default {
  // root node
  el: "#app",
  // the instance state
  data: function () {
    return {
      /** My variables **/
      modal: false,
      drugs: alldrugs,
      drugSearch: "",
      dropdown: { height: 0 },
      filters: { conditions: {}, classes: {}, costs: {} },
      menus: { conditions: false, classes: false, costs: false },
      infoDisplay: {},
    };
  },
  computed: {
    activeMenu() {
      return Object.keys(this.menus).reduce(
        ($$, set, i) => (this.menus[set] ? i : $$),
        -1
      );
    },
    filteredItems() {
      let { conditions, classes, costs } = this.activeFilters;

      return this.drugs.filter(({ Condition, Name, Class, Cost }) => {
        if (conditions.length) {
          let c_split = Condition.split(",");
          console.log("intersect:" + Name);
          console.log(c_split.filter((value) => conditions.includes(value)));
          if (c_split.filter((value) => conditions.includes(value)).length == 0)
            return false;
        }
        if (classes.length && !~classes.indexOf(Class)) return false;
        if (costs.length && !~costs.indexOf(Cost)) return false;

        return Name.toLowerCase().indexOf(this.drugSearch.toLowerCase()) > -1;
      }); // end filter
    },
    activeFilters() {
      let { conditions, classes, costs } = this.filters;

      return {
        classes: Object.keys(classes).filter((c) => classes[c]),
        conditions: Object.keys(conditions).filter((c) => conditions[c]),
        costs: Object.keys(costs).filter((c) => costs[c]),
        //        rating: (this.filters.rating > this.rating.min) ? [this.filters.rating] : []
      };
    },
  },
  methods: {
    changeInfo(drug) {
      this.infoDisplay[drug] = !this.infoDisplay[drug];
      console.log(`Changed info for ${drug}: ${this.infoDisplay[drug]}`);
    },
    setFilter(filter, option) {
      if (filter === "conditions") {
        this.filters[filter][option] = !this.filters[filter][option];
      } else {
        setTimeout(() => {
          this.clearFilter(filter, option, this.filters[filter][option]);
        }, 100);
      }
    },

    clearFilter(filter, except, active) {
      if (filter === "rating") {
        this.filters[filter] = this.rating.min;
      } else {
        Object.keys(this.filters[filter]).forEach((option) => {
          this.filters[filter][option] = except === option && !active;
        });
      }
    },

    clearAllFilters() {
      Object.keys(this.filters).forEach(this.clearFilter);
      this.drugSearch = "";
    },

    setMenu(menu, active) {
      Object.keys(this.menus).forEach((tab) => {
        this.menus[tab] = !active && tab === menu;
      });
    },
  },

  watch: {
    activeMenu(index, from) {
      if (index === from) return;

      this.$nextTick(() => {
        if (!this.$refs.menu || !this.$refs.menu[index]) {
          this.dropdown.height = 0;
        } else {
          this.dropdown.height = `${
            this.$refs.menu[index].clientHeight + 16
          }px`;
        }
      });
    },
  },
  beforeMount() {
    this.drugs = alldrugs;
    this.drugs.forEach(({ Name, Condition, Cost, Class }) => {
      this.$set(this.filters.classes, Class, false);
      this.$set(this.filters.costs, Cost, false);
      this.$set(this.infoDisplay, Name, false);
      Condition.split(",").forEach((cond) => {
        this.$set(this.filters.conditions, cond, false);
      });
    });
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Source+Code+Pro:300,400");
@import url("https://fonts.googleapis.com/css?family=Montserrat");

.more-link {
  float: right;
}

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition-duration: 0.5s;
  transition-property: height, opacity, transform;
  transition-timing-function: cubic-bezier(0.55, 0, 0.1, 1);
  overflow: hidden;
}

.slide-left-enter,
.slide-right-leave-active {
  opacity: 0;
  transform: translate(2em, 0);
}

.slide-left-leave-active,
.slide-right-enter {
  opacity: 0;
  transform: translate(-2em, 0);
}

/******/

.slide-enter-active {
  transition: all 0.2s cubic-bezier(0.55, 0.085, 0.68, 0.53);
}

.slide-leave-active {
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.slide-enter,
.slide-leave-to {
  transform: scaleY(0) translateZ(0);
  opacity: 0;
}

hr {
  border: 0px;
  height: 1px;
  background-color: #e0e0e0;
  margin: 15px 0px 6px 0px;
}

.card {
  transition: all 0.3s ease;
}

.name__filter {
  padding-left: 15px;
}

input {
  border: 1px solid #c5d0d1;
  padding: 0.01em;
  border-radius: 5px;
  height: 20px;
  padding: 5px;
}

h1 {
  margin-left: 0.75em;
  margin-top: 0.75em;
}

* {
  box-sizing: inherit;
  margin: 0;
  padding: 0;
  border-radius: 0;
  border: none;
  outline: none;
  background: none;
  -webkit-margin-before: 0;
  -webkit-margin-after: 0;
  -webkit-margin-start: 0;
  -webkit-margin-end: 0;
  -webkit-padding-before: 0;
  -webkit-padding-start: 0;
  -webkit-padding-end: 0;
  -webkit-padding-after: 0;
}

p {
  display: block;
  margin-block-start: 1em;
  margin-block-end: 1em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
}

ul {
  display: block;
  list-style-type: disc;
  margin-block-start: 1em;
  margin-block-end: 1em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  padding-inline-start: 40px;
}

ul li:not(:last-child) {
  padding-bottom: 0.5em;
}

menu {
  list-style: none;
}

*,
*::after,
*::before {
  box-sizing: border-box;
}

body {
  color: #000;
  background: #fff;
  /*
  background: linear-gradient(
    180deg,
    rgba(86, 216, 228, 1) 10%,
    rgba(159, 1, 234, 1) 90%
  );
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", Helvetica, Arial,
    sans-serif;
  */
  font-family: Montserrat, -apple-system;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

html,
body,
.container {
  min-height: 100vh;
}

a {
  color: #2c3e50;
  text-decoration: none;
}

header {
  position: relative;
  height: 150px;
  padding-top: 100px;
}

header h1 {
  text-align: center;
  font-size: 2.4rem;
  font-weight: 300;
}

/*
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
*/

.debug {
  border-radius: 4px;
  margin: 50px auto;
  width: 500px;
  background-color: #000;
  padding: 50px;
  background: rgba(0, 0, 0, 0.8);
  box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.3);
}

.debug pre {
  color: #ffffff;
  font-size: 18px;
  line-height: 30px;
  font-family: "Source Code Pro", monospace;
  font-weight: 300;
  white-space: pre-wrap;
}

@-webkit-keyframes cd-bounce {
  0%,
  100% {
    -webkit-transform: scale(1);
  }
  50% {
    -webkit-transform: scale(0.8);
  }
}
@-moz-keyframes cd-bounce {
  0%,
  100% {
    -moz-transform: scale(1);
  }
  50% {
    -moz-transform: scale(0.8);
  }
}
@keyframes cd-bounce {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.8);
  }
}

/** MY CSS **/

.card a {
  color: #3498db;
  text-decoration: none;
}
/*
.card a:hover {
  box-shadow: 3px 3px 8px hsl(0, 0%, 80%);
}
*/

.card-content {
  padding: 1.4em;
}

.card-content h2 {
  margin-top: 0;
  margin-bottom: 0.1em;
  font-weight: bold;
}

.card-content h3 {
  margin-top: 0;
  margin-bottom: 0.1em;
  font-weight: bold;
}

.card-content p {
  font-size: 80%;
}

/* Flexbox stuff */

.centered {
  display: flex;
  justify-content: space-around;
  flex-shrink: 0;
  width: 100%;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  width: 100%;
}

.card {
  flex: 1 0 500px;
  box-sizing: border-box;
  margin: 1rem 0.25em;
  border-radius: 25px;
  transition: all 0.35s ease-in-out;
  border: 1px solid #c5d0d1;
  background: white;
  margin-bottom: 2em;
}

@media screen and (min-width: 30em) {
  .card {
    max-width: calc(95% - 1em);
  }
}

@media screen and (min-width: 40em) {
  .card {
    max-width: calc(50% - 1em);
  }
}

@media screen and (min-width: 80em) {
  .card {
    max-width: calc(25% - 1em);
  }
}

@import url("https://fonts.googleapis.com/css?family=Montserrat");

.cards-enter {
  transform: scale(0.5) translatey(-80px);
  opacity: 0;
}

.cards-leave-to {
  transform: translatey(30px);
  opacity: 0;
}

.cards-leave-active {
  position: absolute;
  z-index: -1;
}

.nav {
  display: -webkit-box;
  display: flex;
  -webkit-box-pack: justify;
  justify-content: space-between;
  -webkit-box-align: center;
  align-items: center;
  white-space: nowrap;
  margin: 0 1rem;
  padding: 1rem 0.5rem 1rem;
  border-bottom: 1px dotted #c5d0d1;
}
.nav__controls {
  display: -webkit-box;
  display: flex;
}
.nav__icon {
  width: 1rem;
  height: 1rem;
  fill: currentColor;
}
.nav__label {
  position: relative;
  margin-left: 1rem;
  text-transform: capitalize;
  z-index: 1;
  cursor: pointer;
}
.nav__label::after {
  content: "\00d7";
  display: inline-block;
  color: transparent;
  width: 0.5rem;
  font-weight: 900;
  font-size: 100%;
  -webkit-transform: scale(0);
  transform: scale(0);
  -webkit-transition: -webkit-transform 150ms ease-in-out;
  transition: -webkit-transform 150ms ease-in-out;
  transition: transform 150ms ease-in-out;
  transition: transform 150ms ease-in-out, -webkit-transform 150ms ease-in-out;
}
.nav__label--clear {
  color: #f68185;
  opacity: 0;
  -webkit-transform: translate3d(-25%, 0, 0);
  transform: translate3d(-25%, 0, 0);
  pointer-events: none;
  -webkit-transition: all 275ms ease-in-out;
  transition: all 275ms ease-in-out;
}
.nav__label--filter ~ .nav__label--clear {
  opacity: 1;
  -webkit-transform: translate3d(0, 0, 0);
  transform: translate3d(0, 0, 0);
  pointer-events: auto;
}
.nav__label--filter::after,
.nav__label--active::after {
  -webkit-transform: scale(1);
  transform: scale(1);
}
.nav__label--filter::after {
  content: "\2022";
  color: #46d2c4;
}
.nav__label--active::after {
  content: "\00d7";
  color: #f68185;
}

.dropdown {
  position: relative;
  height: 0;
  overflow: hidden;
  -webkit-transition: height 350ms;
  transition: height 350ms;
}
.dropdown::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1rem;
  /*
  background-image: -webkit-gradient(linear, left bottom, left top, from(white), to(rgba(255, 255, 255, 0)));
  background-image: linear-gradient(to top, white, rgba(255, 255, 255, 0));
  */
}
.dropdown-enter,
.dropdown-leave-to {
  opacity: 0;
}
.dropdown-leave,
.dropdown-enter-to {
  opacity: 1;
}
.dropdown-enter-active,
.dropdown-leave-active {
  position: absolute;
  width: 100%;
  -webkit-transition: opacity 200ms ease-in-out;
  transition: opacity 200ms ease-in-out;
}
.dropdown-enter-active {
  -webkit-transition-delay: 100ms;
  transition-delay: 100ms;
}

.filters {
  padding: 0 1rem;
  display: -webkit-box;
  display: flex;
  flex-wrap: wrap;
  -webkit-box-align: start;
  align-items: flex-start;
}
.filters__item {
  margin-top: 0.5rem;
  margin-right: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #c5d0d1;
  border-radius: 6px;
  font-size: 0.8rem;
  line-height: 1.35;
  cursor: pointer;
  -webkit-transition: all 275ms;
  transition: all 275ms;
}
.filters__item:hover {
  border-color: #379a93;
}
.filters__item--active {
  color: white;
  border-color: #379a93;
  background-color: #379a93;
}
.filters__rating {
  width: 100%;
  display: -webkit-box;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  flex-direction: column;
  -webkit-box-align: center;
  align-items: center;
  padding: 1.5rem 0;
}
.filters__range {
  width: 200px;
  margin-top: 1rem;
  color: inherit;
}
.filters__range::-webkit-slider-thumb {
  width: 0.8rem;
  height: 0.8rem;
  margin-top: calc(-0.4rem + 2px);
  border-radius: 100%;
  background-color: currentColor;
}
.filters__range::-webkit-slider-runnable-track {
  width: 100%;
  height: 4px;
  background-image: -webkit-gradient(
    linear,
    left top,
    right top,
    from(white),
    to(#46d2c4)
  );
  background-image: linear-gradient(to right, white, #46d2c4);
}

.modal {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  display: -webkit-box;
  display: flex;
  -webkit-box-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.6);
  z-index: 1;
}
.modal-enter-active,
.modal-leave-active {
  -webkit-transition: opacity 350ms;
  transition: opacity 350ms;
}
.modal-enter,
.modal-leave-to {
  opacity: 0;
}
.modal-leave,
.modal-enter-to {
  opacity: 1;
}
.modal__content {
  position: relative;
  display: -webkit-box;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  flex-direction: column;
  -webkit-box-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  align-items: center;
  width: 90%;
  max-width: 500px;
  min-height: 250px;
  padding: 1.5rem 1rem;
  background-color: white;
  border: 1px solid #c5d0d1;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 0.5rem 1.75rem -0.25rem rgba(61, 83, 88, 0.4);
}
.modal__title {
  font-weight: 400;
  font-size: 1.5rem;
}
.modal__link {
  margin-top: 1.5rem;
  position: relative;
  font-size: 1.2rem;
  font-weight: 300;
  z-index: 0;
}
.modal__link::after {
  content: "";
  width: 100%;
  height: 1px;
  position: absolute;
  bottom: 0;
  left: 0;
  background-color: currentColor;
  z-index: -1;
  -webkit-transition: background-color 225ms ease-out;
  transition: background-color 225ms ease-out;
}
.modal__link:hover::after {
  background-color: #46d2c4;
}
.modal__close {
  position: absolute;
  top: 0.25rem;
  right: 1rem;
  font-size: 1.75rem;
  font-weight: 400;
  opacity: 0.5;
  -webkit-transition: opacity 150ms ease-out;
  transition: opacity 150ms ease-out;
}
.modal__close:hover {
  opacity: 1;
}
</style>