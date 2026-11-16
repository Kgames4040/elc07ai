"""
Builds the complete Academic Wordlist JSON including Core and Pathways 3 Units 1-10.
"""
import json
import re

raw_table = """
| INTERMEDIATE LEVEL CORE ACADEMIC WORDLIST  <td colspan=7/> |
| #   | HEADWORD   | VERB   | NOUN   | ADJECTIVE   | ADVERB   | COLLOCATION   |
|  | abandon   | abandon   | abandonment   | abandoned   |    | to be left/found abandoned   |
|  | absence   |    | absence   | absent   |    | (to do sth) in/during sb’s absencein the absence of sb/sth to be absent from stha(n) temporary/sudden/unexplained absence(the) absence of data/evidence   |
|  | abstract   |    |    | abstract   |    | abstract idea/concept   |
|  | accommodation   | accommodate   | accommodation   |    |    | to reserve accommodations (somewhere)to provide/offer accommodation   |
|  | accompany   | accompany   |    | accompanied   |    | to accompany sb/sth   |
|  | accurate   |    | accuracy   | accurateinaccurate   | accuratelyinaccurately   | to achieve accuracyaccuracy of sthfairly/entirely/completely accurate  accurate data/ information/descriptions/measurements   |
|  | accuse   | accuse   | accusation   | accusingaccused   |    | to accuse sb of doing sth to be accused of sth accusation against/ofto make an accusation   |
|  | achievement   | achieve   | achievement    |  |  | to achieve success/an objective/a goal/a target  sb’s achievement in (doing) sth  achievement of sth    |
|  | acknowledge   | acknowledge   | acknowledgement   |    |    | to acknowledge mistakes/a person acknowledgement from sb   |
|  | acquire   | acquire   | acquisition   |    |    | to acquire knowledge/skills to acquire assets or propertylanguage acquisition   |
|  | actual   |    |    | actual   | actually   | in actual fact   |
|  | adapt   | adapt   | adaptation   | adaptable   |    | to adapt to sth (successfully/well) to be adaptable a movie adaptation of a book   |
|  | addicted   |  | addiction  addict   | addictive   |  | to be addicted to sth   |
|  | adequate   |    |    | adequateinadequate   | adequatelyinadequately   | to be adequate to do sthto be/to seem (in)adequate for sth   |
|  | adjustment   | adjust   | adjustment   | adjustable   |    | to adjust sthto adjust to sth/doing sthto adjust to a (new)situation/environment an adjustment for/to sthto make a minor/slight/huge adjustment to sthan adjustable chair/seat   |
|  | administer   | administer   | administration   | administrative   |    | to administer tests/first aid/examsadministrative duties   |
|  | admit   | admit   | admission   |    |    | to admit openly/honestly that + sentence to admit to sb (that) to admit (to) doing sthan admission of guilt   |
|  | advance   | advance   | advancement   | advanced   |    | to make a major/rapid advance technological/scientific/medical advance  advancements in science   advanced technology   |
|  | affect   | affect   | effect   | effectiveineffective   | effectivelyineffectively   | to affect sth/sb (greatly) to be/seem effectiveto have a long-term/short-term effect a positive/beneficial/negative/harmful effect on sb/sth   |
|  | affordable   | afford   |  | affordable   |  | affordable housing/costsan affordable price   |
|  | agriculture   |    | agriculture   | agricultural   |    | intensive/extensive/traditional agricultureagricultural land/productionthe agricultural sector                              an agricultural economy   |
|  | aim   | aim   | aim   | aimless   |    | to have/achieve an aimto aim for/at sth   to aim to do sth   |
|  | allocate   | allocate   | allocation   |    |    | to allocate time/money/resources/funds to allocate sth for sth/to sth   |
|  | alter   | alter   | alteration   |    |    | to alter sthto alter one’s perceptionsto make alterations   |
|  | alternative   |    | alternative   | alternative   | alternatively   | to find an alternative to sthalternative music/lifestyle   |
|  | analyze   | analyze   | analysis   |    |    | to analyze data/information/a situationto analyze carefully/in depth/scientifically to do/carry out/conduct an analysis detailed analysis of sth   |
|  | annually   |    |    | annual   | annually   | annual income/reportsannual budget/income/cost   |
|  | anticipate   | anticipate   | anticipation   |    |    | to anticipate a situation/problemto anticipate changes/developments   |
|  | anxiety   |    | anxiety   | anxious   | anxiously   | to cause/create/lead to/reduce/relieve anxiety to be anxious about sth/for sb a source of anxiety anxiety about/over sth   |
|  | apparently   |  |  | apparent   | apparently   | to be/become/seem apparent   |
|  | appearance   | appeardisappearreappear   | appearancedisappearance   reappearance   |    |    | to make an appearanceappearance of sth   |
|  | apply   | apply   | application   |  |  | the application of sth (to sth)  practical/commercial/efficient application  to apply to sb/sth  to apply for sth (a job/visa/license, etc.)  to apply sth to sb/sth   |
|  | apply   | apply   | application   |  |  | the application of sth (to sth)  practical/commercial/efficient application  to apply to sb/sth  to apply for sth (a job/visa/license, etc.)  to apply sth to sb/sth   |
|  | appreciate   | appreciate   | appreciation   |    |    | to appreciate the importance/value of sthto really/fully/deeply appreciate sth or sb to have/show/express/develop appreciation deep/great/real appreciation   |
|  | approach   | approach   | approach   |    |    | to approach sb for sthto approach a problem/task/matter to have/take/adopt/use an approach a new/different/fresh/alternative approach   |
|  | approve   | approve   | approval   | approved   |    | to approve of sth   |
|  | approximately   |    |    | approximate   | approximately   | an approximate amount of time or money   |
|  | arise   | arise   |    |    |    | to arise from sth   |
|  | arrest   | arrest   | arrest   |    |    | to arrest sb   to be arrested for sth   to be under arrest   |
|  | aspect   |    | aspect   |    |    | a key/major/fundamental aspect of sthin every aspect of sth   |
|  | assess   | assess   | assessment   |    |    | to make/give assessmentassessment methods   |
|  | assign   | assign   | assignment   |    |    | to assign sb a task/role/homeworkto assign sb (to) sth/ sth to sbto assign sb to do stha homework assignment   |
|  | assimilate   | assimilate   | assimilation   |    |    | to assimilate sb (into/to sth)   |
|  | assist   | assist   | assistance assistant   |    |    | to give/offer sb assistance to assist with sthto assist sb in doing sth   |
|  | associate   | associate   | association   | associated   |    | to be associated with sth   |
|  | assume   | assume   | assumption   |    |    | to make assumptions about stha wrong/false/mistaken assumptiona common/general/widespread assumption   |
|  | attach   | attach   | attachment   | attached   |    | to have/form/develop attachmentclose/deep attachment   |
|  | attempt   | attempt   | attempt   |    |    | to make an attemptto succeed in/fail in an attempt   |
|  | attitude   |    | attitude   |    |    | to have a good/bad/positive/negative attitudeattitude towards sth an attitude problem   |
|  | attraction   | attract   | attraction   | attractive   | attractively   | to attract attention   |
|  | attribute   | attribute   | attribution   |    |    | attribute sth to sb/sth   |
|  | authority   |    | authority   | authoritative   |    | absolute/complete/full authority   |
|  | autonomously   |    | autonomy   | autonomous   | autonomously   | to gain autonomy from sbto increase/reduce autonomy autonomous learners/cars   |
|  | availability   |    | availability   | availableunavailable   |    | the availability of sb/sthlimited/widespread/growing availability of stha lack of availability of sth   |
|  | award   | award   | award   |    |    | to be awarded sth for sth to receive/win an award   |
|  | aware   |    | awareness   | awareunaware   |    | to have/raise awarenessto be/become aware/unaware of sth a lack of awareness environmental/political/social awareness   |
|  | background   |  | background   |  |  | background information/details/data  (to have) a background in an area/field  in the background   |
|  | bargain   | bargain   | bargain   |  |  | to make/look for/get/find a bargainto bargain for/over sthto bargain with sb   |
|  | barrier   |    | barrier   |    |    | cultural/racial/social barriers barrier to sth/sb   to overcome barriers   |
|  | basically   |    |    | basic   | basically   | the basic principles of sthbasic needs/rights/life skills   |
|  | basis   | base (on)   | basis   | based   |    | on a regular/daily/weekly/monthly basison a voluntary/part-time/temporary basisto base sth on sthto form the basis of sth   |
|  | beneficial   | benefit   | benefit   | beneficial   | beneficially   | to benefit from sth   to have enormous/great benefit   to be beneficial to sb/sth   |
|  | bias   | bias   | bias   | biased   |    | to have a bias against sbpolitical/gender/racial bias   |
|  | blame   | blame   | blame   |    |    | to put the blame on sbto blame sb for sth   |
|  | blend   | blend   | blendblender   |    |    | to blend with sthto blend A with Bto blend A and B (together)a blend of A and B   |
|  | bond    | bond   | bond  bonding   |  |  | (to form/have) a bond with sb/sth/  a bond between A and B  a close/strong/special bond   |
|  | boost   | boost   |    |    |    | to boost sb’s confidence/egoto boost profits/prices/sales/the economyto boost production/performance/productivity   |
|  | bother   | bother   | bother   |    |    | bother to do sth   |
|  | brief   |    |    | brief   | briefly   | fairly brief   |
|  | budget   |    | budget   |    |    | family budgetto be on a budget   |
|  | capable   |    | capability   | capableincapable   |    | to be capable of sth to have capability   |
|  | capacity   |    | capacityincapacity   |    |    | to have/increase capacity to have a capacity for/of sthto operate at full capacitycapacity to do sth   |
|  | care   | care   | care   | carefulcarelesscaring   |    | to take care of sb/sthto provide/receive/need/require careto care about   |
|  | category   | categorize   | category   | categorical   | categorically   | to categorize things or people a categorical denial to categorically deny/reject/refusecategorically untrue/false   |
|  | challenge   | challenge   | challenge   | challenging   |    | significant/technical challengeto challenge sb/sth   |
|  | charge   | charge   |    |    |    | to charge sb with a crimeto charge of/forin charge (of sth)free of charge   |
|  | circumstance(s)   |    | circumstance(s)   |    |    | the circumstances of a situationunder certain circumstances   |
|  | citizen    |  | citizen   |  |  | to become a citizen (of a country)   |
|  | civilized   |    | civilization   | civilizedcivil   |    | civilized behavior/society/worldancient/early civilizations the end/collapse/decline of a civilization   |
|  | claim   | claim   | claim   |    |    | a false claimto claim to do/be sth   |
|  | clarify   | clarify   | clarification   |    |    | to fully/further clarifyto clarify expectations   |
|  | classic   |    | classic   | classical   | classically   | a classic car  a classic example/mistake/case/design  classical music/musician/composer/literature   |
|  | collapse   | collapse   | collapse   |    |    | the collapse of society/economyin the danger of collapsea sudden/economic/mental/physical collapse   |
|  | combination   | combine   | combination   |    |    | to combine x with ya combination of factors/colors   |
|  | combine   | combine   | combination   | combinedcombining   |    | to combine sth with sth   |
|  | commerce   | commerce   | commercial   | commercial   | commercially   | international/domestic commercecommerce between/withcommercial transaction/use/flightglobal commerce   |
|  | commission   |    | commission   |    |    | human rights commissionto set up/establish/create a commissiona special/independent/international commission   |
|  | commit   | commit   | commitment   | committed   |    | to commit suicide/a crime to make a commitmentto show/lack commitmentcomplete/full/lifelong commitment   |
|  | competition   | compete   | competitioncompetitor   | competitive   | competitively   | to be in competition with to compete with/againstmajor/main competitorsto compete for/in/at   |
|  | compile   | compile   | compilation   |    |    | to compile datato compile sth from/for stha compilation album   |
|  | complex   |    | complexity   | complex   |    | a highly complex systemthe complexity of a situation   |
|  | complicated   | complicate   | complication   | complicateduncomplicated   |    | highly/terribly complicated   |
|  | component   |    | component   |    |    | components of sthkey/major/important component   |
|  | comprehensive   | comprehend   | comprehension   | comprehensive   |    | comprehensive review/study/survey/reportcomprehensive information/plan/health care service   |
|  | concentration   | concentrate   | concentration   | concentrated   |    | to concentrate on/upon sth to require/lose concentrationto be totally concentrated on sth deep/great concentrationa large/high/small/low concentration of sththe concentration of sth increases/decreases   |
|  | concept   |    | concept   | conceptual   |    | to have a concept of sth a legal/mathematical/marketing conceptconceptual art   |
|  | concern   | concern   |    | concerned   |    | to be concerned with   |
|  | conclude   | conclude   | conclusion   | conclusive   |    | to conclude sth  in conclusion  conclusive proof/evidence/findings   |
|  | concrete   |    |    | concrete   |    | concrete proposal/proof/evidence   |
|  | condition   |  | condition   |  |  | in a good/poor/excellent/terrible/critical condition  physical/mental/medical condition  a necessary condition for/of sth  living/working conditions   |
|  | conduct   | conduct   | conduct   |    |    | to conduct a survey/experiment   |
|  | confirm   | confirm   | confirmation   | confirmed   |    | confirmation of an appointmentto wait for/have/get confirmation   |
|  | conflict   |    | conflict   | conflicting   |    | constant conflicta conflict of interestsconflicting information/results   |
|  | confused   | confuse   | confusion   | confusing confused   |    | to easily confuse sb with sb to cause/create/result in confusion about sth to be/become/seem confused about sth   |
|  | conscious   |    | conscious (psychology)consciousness   | conscious   | consciously   | half-consciousconscious of (doing) sth   |
|  | consequently   |    | consequence   | consequent   | consequently   | to have dangerous/serious/consequences to lead to/suffer/face consequences as a consequence of sthsocial/political/economic consequences   |
|  | conservation   |    | conservation   |    |    | conservation of sthwildlife/nature/environmental conservationconservation policies/measuresa conservation group/project/program   |
|  | consider   | considerreconsider   | considerationreconsideration   |    |    | to take into considerationto consider carefully/seriouslyto reconsider (the) decisions   |
|  | considerably   |    |    | considerable   | considerably   | to vary/differ/improve/increase/decrease considerablya considerable amount/number of stha considerable effect/variation/differenceto take sth into considerationto deserve/require (serious/careful) consideration    |
|  | consist of   | consist of   |    |    |    | to consist entirely/mainly/largely of sth   |
|  | consistent   |    | consistency   | consistentinconsistent   | consistentlyinconsistently   | to be (in) consistent with sthconsistent in stha lack of consistency in sth   |
|  | constantly   |    |    | constant   | constantly   | to remain constant   |
|  | constrain   | constrain   | constraint   |    |    | to be constrained by sb or sthto impose/place constraints on sb/sthfinancial/environmental/political constraints   |
|  | construct   | construct   | construction   | constructive   |    | to give constructive advice/criticism   |
|  | consultant   | consult   | consultantconsultancy   |    |    | to consult sb about sthto receive consultancya consultancy firm/business   |
|  | consumption   | consume   | consumer  consumption  consumerism   | consumer   |    | consumer rights  to protect/satisfy consumer   to boost/increase/reduce consumption   high/low consumption   |
|  | contemporary   |    | contemporary   | contemporary   |    | contemporary music/art/dance   to be a contemporary of someone elsecontemporary society/lifecontemporary artists/writers   |
|  | contribute   | contribute   | contributioncontributor   |    |    | to make a contribution to sthto contribute to sth an important/big/major contribution   |
|  | controversy   |    | controversy   | controversial   | controversially   | to cause/create controversycontroversy over/abouthighly controversiala controversial plan/proposal/policy/decision/issue   |
|  | convenient   |    | convenience   | convenientinconvenient   | convenientlyinconveniently   | highly (in)convenientmutually convenient   |
|  | conventional   |    |    | conventional   | conventionally   | highly/quite/strictly conventional conventional behavior   |
|  | conversation   | converse   | conversation   |    |    | to have a conversation with sb/about sthto converse with sb   |
|  | convert   | convert   | conversion   | convertible   |    | to convert sb to a religionto convert a building from one type to anothera convertible sofa/cara convertible currency   |
|  | convince   | convince   |    | convincing convinced   |    | to make a convincing argument to convince sb to do sth   |
|  | coordination   | coordinate   | coordination   |    |    | coordination of sthto coordinate sthto coordinate with sb   |
|  | cope   | cope (with)   |    |    |    | to cope successfully   to cope with sth/sb   |
|  | corporate   |    | corporation   | corporate   |    | a corporate trainer/jobcorporate culture/identity/sector/profits   |
|  | credit   |    | credit   |    |    | to get/deserve/receive/take/claim the creditto buy/get sth on credit   |
|  | crisis   |  | crisis   |  |  | a(n) economic/political/personal crisis  crisis management  to go through/suffer a crisis  to be in crisis   |
|  | critical   | criticize   | criticism   | critical   | critically   | to criticize sb for stha critical comment/reportcritical thinking   |
|  | crucial   |  |  | crucial   | crucially   | crucial to/for sth  a crucial decision/step/aspect  to play a crucial role in doing sth  a crucial piece of informationcrucial for/to sb/sth   |
|  | cure   | cure   | cure   | curableincurable   |    | a cure for an illness/povertyto find a cureto cure sb of sth   |
|  | curiosity   |    | curiosity   | curious   | curiously   | great/natural/intellectual curiosityto have curiosity about sthto satisfy sb’s curiosityout of curiosity   |
|  | current   |    |    | current   | currently   | current condition/situation/population   |
|  | debt   |    | debt   |    |    | to be (heavily/deeply) in debt (to sb/sth)  to get/go/fall into debt  to pay off/claim a debt   |
|  | decade   |    | decade   |    |    | decades long   |
|  | decay   | decay   | decay   |    |    | to decay slowly/rapidlythe process/signs of decay   |
|  | declare   | declare   | declaration   |    |    | to declare victory/war/bankruptcy   |
|  | decline   | decline   | decline   |    |    | to decline in importance/size steep/steady/sharp decline in sth the decline of a civilization   |
|  | define   | define   | definition   |    |    | to define sth as sthclearly/well defineddefinition of sth   |
|  | definitely   |    |    | definiteindefinite   | definitelyindefinitely   | a definite improvement/promiseone can definitely say (that)postpone indefinitely   |
|  | deliberate   |    |    | deliberate   | deliberately   | the deliberate use of stha deliberate attempt/ decision   |
|  | demonstrate   | demonstrate   | demonstration   |    |    | to demonstrate for/against sthto demonstrate how/what/why   |
|  | deny   | deny   | denial   | deniabledenied   |    | to deny (that)to deny doing sth   |
|  | dependent   | depend   | dependency dependence independence   | dependent independent   | independently   | dependency on sth/sb to depend on sth/sb to be dependent on/upon sth/sb (for sth)   |
|  | depressed   | depress   | depression   | depressivedepressing   | depressively   | a depressed person/economyeconomic depression   a depressive personalitya depressing situation   |
|  | deserve   | deserve   |    |    |    | well-deservedto deserve to do sthto deserve respect/credit/support/recognition   |
|  | destruction   | destroy   | destruction   | destructive   |    | the environmental/habitat destruction   |
|  | detect   | detect   | detection   |    |    | to detect illnesses   |
|  | determine   | determine   | determination   | determined   |    | to determine to do sthto have/show determination  absolute/strong/clear determinationto show/be full of/require/lack determination   |
|  | deviate   | deviate   | deviation   |    |    | to deviate from sthdeviation from   |
|  | diagnose   | diagnose   | diagnosis   |  |  | a doctor’s diagnosisto diagnose an illness   |
|  | digest   | digest   | digestion   | digestivedigestible   |    | good/poor digestiondigestive system/organs/juices etc.easily digestible food   |
|  | dilemma   |    | dilemma   |    |    | a dilemma about/over stha dilemma between A and Bin a dilemma   |
|  | dimension   |    | dimension   | dimensional   |    | to have many dimensions  to add a new/an extra/another dimension (to sth)  political/social/economic dimension  three-dimensional/ (3D)   |
|  | disaster   |    | disaster   | disastrous   |    | natural/major disasterdisaster recovery/reliefdisastrous for (the economy)   |
|  | discouraged    | discourage   |  | discouraged  discouraging   |  | to discourage sb from doing sth  discouraging results/news   |
|  | discrimination   | discriminate   | discrimination   |    |    | to discriminate against sb/a group of peopleage/racial/genetic discrimination   |
|  | dishonest   |  | dishonesty   | dishonest   |  | a dishonest way of doing sth   |
|  | dismiss   | dismiss   | dismissal   |    |    | to dismiss an idea/the class   |
|  | display   | display   | display   |    |    | to display sth (talents/paintings/the latest fashions, etc.)to be/go on display   |
|  | disrupt   | disrupt   | disruption   | disruptive   |    | to be disrupted by sth to cause (serious/widespread) disruption   |
|  | distinguish   | distinguish   |    | distinguished   |    | to distinguish sb/sth from sb/stha distinguished person/career   |
|  | distract   | distract   | distraction   | distractingdistracted   |    | to distract sb from sthto create a distraction   |
|  | distribute   | distributeredistribute   | distributionredistribution   |    |    | redistribution of wealth/resources to distribute sth among/to sbto distribute fairly/equally   |
|  | diversity   |    | diversity   | diverse   |    | cultural/ethnic/biological/genetic/religious diversitygreat/wide/immense diversity  to create/protect diversitydiversity of sthto encourage/promote diversity   |
|  | document   | document   | documentation   | documented   |    | to have documentation of/for sth   |
|  | domestic   | domesticate   | domestication   | domestic   | domestically   | domesticate an animaldomestic flights/animals   |
|  | dominant   | dominate   | dominance   | dominant   |    | to dominate a person or situationto achieve/assert dominance over to seem/become/remain dominant   |
|  | donate   | donate   | donation   |    |    | to donate money/blooda generous/small/public/private donationto make a donation   |
|  | dramatically   |    |    | dramatic   | dramatically   | to improve/increase/reduce/decrease dramaticallydramatic impact/decrease   |
|  | dynamic   |    |    | dynamic   | dynamically   | a dynamic person/personality   |
|  | economy   |    | economyeconomics   | economiceconomical   | economically   | economic policies/factors/state/crisiseconomical car/way   |
|  | education   | educate   | education educator   | educateduneducatededucational   |    | to educate sb about/in/on sthto have/receive education private/public educationuniversity-educated/well educated/privately educated   |
|  | effective   |    | effect   | effectiveineffective   | effectivelyineffectively   | partially effective   |
|  | efficiency   |    | efficiency   | efficientinefficient   | efficientlyinefficiently   | to look/appear efficient the efficient use of sthto improve/increase/promote efficiencyenergy/fuel-efficient cost-efficient   |
|  | eliminate   | eliminate   | elimination   |    |    | to eliminate sth (from sth)   |
|  | emerge   |    | emerge   |    |    | to emerge from sth   |
|  | emphasize   | emphasize   | emphasis   |    |    | to place emphasis on   |
|  | enable   | enable   |    |    |    | to enable sb/sth to do sth   |
|  | encounter   | encounter   | encounter   |    |    | to encounter a problem/difficulty   |
|  | enhance   | enhance   | enhancement   |    |    | to enhance performance/productivityto enhance sb’s skillan enhanced ability   |
|  | ensure   | ensure   |    |    |    | to ensure sb’s safety   |
|  | enthusiastic   |    | enthusiasm   | enthusiastic unenthusiastic   | enthusiastically unenthusiastically   | to have/show/lose enthusiasm (for sth) great/little enthusiasm   |
|  | entire   |    | entirety   | entire   | entirely   | in one’s entire lifeentire world/familyin its/their entirety   |
|  | equally   |    | equality inequality   | equal unequal   | equallyunequally   | to have equality to be/become equal equal number/amount (of sth) equal in size/length/height   racial/gender/social/economic equality/inequalityto be equally important   |
|  | era   |    | era   |    |    | the modern/present/current eraa golden era (in history)the end of an erato enter a new era (of sth)   |
|  | essential   |    |    | essential   | essentially   | essential to/for sthit is essential to do sth   |
|  | establish   | establish   | establishment   |    |    | to establish a company/an organizationto establish relations/links/contact (with sb)the political/military/medical establishment   |
|  | estimate   | estimate   | estimateestimation   |    |    | an estimation of costsan early/initial/rough/current estimate   to make an estimate   |
|  | ethnicity   |    | ethnicity   | ethnic   | ethnically   | ethnic origin/groups/clothes/jewelry/food   |
|  | evaluation   | evaluate   | evaluation   | evaluative   |    | to evaluate performanceevaluation processto carry out an evaluation   |
|  | eventually   |    |    | eventual   | eventually   | eventual destructioneventual outcome/successsb eventually does sth   sth eventually happens   |
|  | evident   |    | evidence   | evident   | evidently   | to become (clearly) evidentto be evident to sb  evidence for/of/against sth   |
|  | evolve   | evolve   | evolution   | evolutionary   |    | to evolve from/into/out of sthevolution ofevolutionary theory   |
|  | examine   | examine   | examination   |    |    | to carefully/closely examinea medical examinationunder examination   |
|  | exceed   | exceed   | excess   | excess   |    | to exceed one’s capacity/expectations   to exceed the speed limit   |
|  | executive   |    | executive   |    |    | executives of corporationsa senior executive   |
|  | exhibit   | exhibit   | exhibition   |    |    | to exhibit tendencies/symptoms/signs ofto exhibit artwork   |
|  | exist   | exist   | existence   | existing   |    | human existenceto bring sth into existence   |
|  | expand   | expand   | expansion   |    |    | to expand into/on/upon sth expansion of/in sthrapid expansion   |
|  | expense   |    | expense   | expensive   | expensively   | monthly/living expense(s)the extra/additional expense   |
|  | expertise   |    | expertiseexpert   | expert   |    | to have expertise in sth   |
|  | explicitly   |    |    | explicit   | explicitly   | to be explicit about sthexplicitly forbidden   |
|  | exploit   | exploit   | exploitation   |    |    | to exploit resources (positive)to exploit a person (negative)   |
|  | expose   | expose   | exposure   |    |    | to expose someone to sthto be exposed to sthhigh/massive/excessive exposure   |
|  | extend   | extend   | extension   |    |    | to extend an area/road/deadline/visa   |
|  | extent   |    | extent   |    |    | to understand/realize the (actual) extent of sthto some extent/to a certain extent to a large/great extent   |
|  | external   |    |    | external   | externally   | external factors   |
|  | extinct   |    | extinction   | extinct   |    | to go/become extinctextinct species/animalsin danger of extinction   |
|  | extract   | extract   | extract extraction   |    |    | to extract sth from sth to extract information/data an extract from (a book/a song)the extraction of minerals/natural resources   |
|  | extreme    |  |  | extreme   | extremely   | extreme weather/temperatures   extreme conditions/sports/poverty  in extreme cases   |
|  | facilitate   | facilitate   | facilitator   |    |    | to facilitate communication/a discussion/a negotiation a facilitator for a negotiation   |
|  | failure   | fail   | failure   |    |    | a complete failureheart/kidney/liver failureto fail to do sth to fail a test   |
|  | fascinating    |  |  | fascinating  fascinated   |  | a fascinating/movie/documentary/lecture/discovery   |
|  | feature   | feature   | feature   |    |    | to regularly/rarely feature essential/important/key/main/common features of sth   |
|  | feedback   |    | feedback   |    |    | to give/provide (positive) feedback (to sb)to receive/get feedback (from sb)   |
|  | finance   | finance   | finance (dealing with money and banking)   | financial   | financially   | to finance a businessa financial advisor   |
|  | flexible   |    | flexibility   | flexibleinflexible   |    | to be (in) flexible about sthextremely/highly/fairly flexible   |
|  | flow   |  | flow   |  |  | the flow of sth  to go with/against the flow   |
|  | force   | force   | force   |    |    | to force sb to do sth   with great/considerable/increasing force   by force  police force/air force/armed forces/workforce   |
|  | forecast   | forecast   | forecast   |  |  | weather forecastsales/profit forecastto make a forecast   |
|  | framework   |    | framework   |    |    | constitutional/organizational framework   |
|  | fulfillment   | fulfil   | fulfillment   | fulfilled   |    | to fulfil your dream/ambition/ potentialto fulfil a duty/ promise   |
|  | functional   | function   | function   | functional   |    | to perform/fulfil a functiona function of sthto function normally/correctly/properly   |
|  | fundamental   |    | fundamental(s)   | fundamental   | fundamentally   | to seem/remain/consider sth/regard sth as fundamental  a fundamental change   |
|  | funding   | fund   | funding   | funding   |    | government/education/research funding   |
|  | gain   | gain   | gain   |    |    | to gain control/power/reputation financial/economic gainto gain sth from (doing) sth   |
|  | gather   | gather   | gathering   |    |    | to quickly/slowly gathera formal gathering   |
|  | generate   | generate   | generation   |    |    | to generatethe generation of revenue/ideas/electricity/energy/ excitement/interestto support the older/younger generationa generation gap   |
|  | global   |    | globe   | global   | globally   | global reach   |
|  | gradually   |    |    | gradual   | gradually   | a gradual increase/decrease   |
|  | grant   | grant   | grant   |    |    | grant sb sth grant sth to sb a government/research/student grant   |
|  | growth   | grow   | growth   |  |  | to grow fruit/vegetables/flowers/plantspopulation growth   |
|  | harm   | harm   | harm   | harmful harmless   |    | to do/cause harm harmful to sth (the environment/one’s health, etc.)there’s no harm in doing sthharmful effects/results   |
|  | heal   | heal   |  |  |  | to heal slowly/quickly  to take a long time to heal   |
|  | hesitate   | hesitate   | hesitation   | hesitant   |    | to hesitate a little/a moment to hesitate about sth a brief/slight/momentary hesitation   |
|  | hierarchy   |    | hierarchy   | hierarchical   | hierarchically   | organizational/social/strict hierarchyto create/establish/rise in hierarchy   |
|  | highlight   | highlight   | highlight   | highlighted   |    | to clearly highlight   |
|  | hypothesize   | hypothesize   | hypothesis   | hypothetical   | hypothetically   | to make a hypothesis a hypothetical situation/example/questionto prove/test/support a hypothesis   |
|  | identical   |    |    | identical   | identically   | to be identical to sb/sthto be identical in sthidentical twins   |
|  | identify   | identify   | identificationidentity   | identifiedunidentified   |    | to identify sb/sthto identify with sb /sth with sban identity cardidentity card national/cultural/social identityto find out/discover somebody’s identity   |
|  | ignore   | ignore   | ignorance   | ignorant   |    | to be/cannot be difficult to ignore  to be ignorant of/about   |
|  | illegal   |    |    | legal illegal   | legally illegally   | legal action/right/advice/profession/system   |
|  | illustrate   | illustrate   | illustration   |    |    | a good/perfect illustration of sth   |
|  | imitate   | imitate   | imitation   |    |    | a/an accurate/poor/cheap imitation of sthin imitation of sb/sthto imitate sb/sth   |
|  | impact   | impact   | impact   | impactful   |    | to impact on sth /sth to have/create an impact on sthto have a big/considerable/dramatic impact   |
|  | implement   | implement   | implementation   |    |    | to implement sth fully/properly/effectively to implement a law/system/plan/changes effective/successful/complete implementation   |
|  | implication   | imply   | implication   |    |    | the implications of an actionconsiderable/crucial/major/important implications   |
|  | import   | import   | import   |    |    | to import sth from somewhereto import from/into sthto increase/reduce/cut importsagricultural imports   |
|  | impose   | impose   |    | imposing   |    | to impose sth on someone   |
|  | impressed   | impress   | impression   | impressedimpressive   | impressively   | to impress sb with sthto make/ give/create/leave an impression on sba good/positive/bad/negative impressiona false impression   |
|  | inappropriate   |    | appropriatenessinappropriateness   | appropriateinappropriate   | appropriatelyinappropriately   | at an (in)appropriate time/placean (in)appropriate behaviorto be (in)appropriate for sth   |
|  | incentive   |    | incentive   |    |    | to create/provide/give sb an incentive to have/lack an incentive to do sth economic/financial/tax incentives   |
|  | incident   |    | incident   |    |    | without incidenta serious/major/small/minor incidentan incident happens/occurs   |
|  | income   |    | income   |    |    | annual incomea high/low income   |
|  | incorporate   | incorporate   | incorporation   |    |    | to incorporate sth into sth   |
|  | incredible   |    |    | incredible   | incredibly   | pretty/really/truly/absolutely/quite incredibleto be/look/smell/taste/find sth incredibleat an incredible rate/speed   |
|  | indicate   | indicate   | indicationindicator   |    |    | regard/see sth as an indication of sth   |
|  | individual   |  | individual   | individual   | individually   | work/study/do sth individually  individual needs  to treat sb (people) as individuals  an individual preference/choice   |
|  | inevitable   |    | inevitability   | inevitable   | inevitably   | an inevitable result/consequence   |
|  | infected   | infect   | infection   | infectious infected   |    | to have/suffer from/develop an infection to treat/fight an infection infectious disease to get/become infected heavily   |
|  | inferior   |    |    | inferior   |    | to make sb feel inferiorinferior to sb/sth   |
|  | influence   | influence   | influence   | influential   |    | to be under the influence of sthto have a good/bad influence on sb to influence sb to do sth  influential in doing sth   |
|  | inherit   | inherit   | inheritorinheritance   |    |    | an inheritor of a large sum of moneyto inherit sth from sbto live off one’s inheritance   |
|  | initially   |    |    | initial   | initially   | an initial investment/an initial impression/reaction   |
|  | initiative   | initiate   | initiative   |    |    | to plan/develop/introduce/launch an initiative to have the initiative to do sth   |
|  | innocence   |    | innocence   | innocent   |    | innocent intentions/people/questions   |
|  | innovative   | innovate   | innovatorinnovation   | innovative   |    | successful/scientific/technological innovationinnovative ideas   |
|  | insert   | insert   | insertion   |    |    | to insert sth (in/into sth)   |
|  | insight   |    | insight   |    |    | to provide/give an insight into sth   to offer insight   |
|  | insist   | insist   | insistence   | insistent   |    | to insist on doing sthinsistence on sth   |
|  | inspire   | inspire   | inspiration   | inspiredinspiringinspirational   |    | to inspire sb with sthto give sb inspirationto provide sb with inspiration   |
|  | install   | install   | installation   |    |    | to install software/an appto install sth on sth   |
|  | institute   |    | institutioninstitute   | institutional   |    | an institute of higher learning (university)financial/educational/research etc institutionthe institution of marriage/monarchy   |
|  | integrate   | integrate   | integrationdisintegration   | integrated   |    | to integrate into/with sthto integrate racially/completely/successfullyto integrate sth into sth   |
|  | intense   |    |    | intense   | intensely   | intense feelings/emotions/pressurean intense desireto dislike intensely   |
|  | intention   | intend   | intention   | intentional unintentional   | intentionally unintentionally   | to intend to do sth intention to do sthto have no/every intention of doing sth   |
|  | interact   | interact   | interactioninteractivity   | interactive   | interactively   | to interact with sbinteraction between/among sb/sthan interactive activity   |
|  | interfere   | interfere   | interference   |    |    | to interfere with sb/sth/ in sth   |
|  | interpret   | interpret   | interpretation   |    |    | to interpret correctly/wrongly/differently to make an interpretation to interpret sth as sthto be open to interpretation interpretive dance   |
|  | interrupt   | interrupt   | interruption   |    |    | without interruptions   |
|  | investigation   | investigate   | investigation   investigator   |    |    | to investigate carefully/closely to carry out/conduct an investigationunder criminal investigation   |
|  | investment   | invest   | İnvestment  investor   |    |    | to invest in sth to invest time/money/energy in sth good/excellent/profitable/good/sound investment   |
|  | involve   | involve   | involvement   | involved   |    | someone’s involvement in a situationto involve sb (in sth/in doing sth)to be/get involved in sth   |
|  | irony   |    | irony   | ironic   | ironically   | tragic/cruel/bitter irony   |
|  | issue   |    | issue   |    |    | to have an issue with sth   |
|  | justice   | justify   | justicejustification   | justified justunjustified unjust   |    | social justiceto want justiceto justify doing sthto justify a policy/the means/the effort/the need for   |
|  | lack   | lack   | lack   |    |    | to lack sth (confidence, etc.) lack of food/money   |
|  | landscape   |  | landscape   |  |  | a(n) natural/rural/industrial/urban landscape  political/social landscape   |
|  | launch   | launch   | launch   |    |    | to officially launch stha missile/rocket launchthe launch of the campaign/website/service   |
|  | layer   |    | layer   |    |    | layer upon layerto wear layers the ozone layer   |
|  | livelihood   |    | livelihood   |    |    | a means (of)/sources (of) livelihoodto earn/lose a livelihoodto protect livelihoods   |
|  | logical   |    | logic   | logicalillogical   | logicallyillogically   | a logical conclusion   |
|  | lower   |    |    |    |    | to lower sb’s voiceto lower the rate/cost/price/level of sth   |
|  | maintain   | maintain   | maintenance   |    |    | to maintain an ideal weight/a building to carry out/need/require maintenance   |
|  | manual   |    |    | manual   | manually   | manual job/labor/worker   |
|  | manufacture   | manufacture   | manufacture manufacturing manufacturer   |    |    | to manufacture products/goods large-scale/industrial manufacturing car/food manufacturingto manufacture sth from sth   |
|  | measure   | measure   | measure  measurement   |  |  | a(n) accurate/detailed measurement of sth  to take measures (to do sth)   |
|  | mental   |  | mentality   | mental   | mentally   | mental health/problem/illness/disorder/well-beingmental ability/capacitymentally healthy/ill   |
|  | merge   | merge   |    |    |    | to merge into/with sthto merge sth with sth   |
|  | method   |    | methodology   | methodological   | methodologically   | the methodology of an experiment methodology for (doing) sthscientific methodology   |
|  | minor   |    |    | minor   |    | a minor injury/illness/operation/problem   |
|  | minority   |    | minority   | minority   |    | a minority group/opinion   |
|  | mission   |  | mission   |  |  | (to go) on a mission  the main/core mission (of a company/organization)   |
|  | mode   |    | mode   |    |    | a mode of transportation mode of instruction   |
|  | modify   | modify   | modification   | modifiable modified   |    | genetically-modified foodto modify a design/a gene/the behavior   |
|  | monitor   | monitor   | monitor   |    |    | to monitor a situation   |
|  | moral   |    | morality   | moralimmoral   | morally   | a moral issue/dilemmamorally right/wrong/justified/unacceptable   |
|  | motive   | motivate   | motivationmotive   | motivational   | motivationally   | poor/low motivationto lack/lose motivationmotivation/motive for (doing) sth  motive behind (sth)   |
|  | natural   |    | nature   | natural   |    | natural selection/beauty to be natural   |
|  | negate   | negate   | negation   |    |    | to negate sth   |
|  | negotiate   | negotiate   | negotiation   |    |    | to negotiate with sb for/about sthto negotiate a deal/ contract   |
|  | notice   | notice   | notice   | noticeable   |  | advance/prior notice  to give notice of sth   to do sth at short notice/ without notice  a noticeable change/improvement in sth/sb    |
|  | notion   |    | notion   |    |    | to have a notion about sththe notion of sth   |
|  | numerous   |    |    | numerous   |    | numerous articles/publications/studies   |
|  | nutrition   |    | nutritionnutrient   | nutritious   |    | a nutritious dietadequate/good/proper nutritiona source of nutrition   |
|  | obey   | obey   | obedience   | obedientdisobedient   | obediently   | to obey rules   |
|  | objective   |    | objective   |    |    | to set/achieve an objectiveto reach/meet an objectivethe main/principal/primary/prime objectivea key/clear objective   |
|  | obligation   |    | obligation   | obligedobligatory   |    | to be/feel obliged to do sthto be obligatory for sb to do sthto have/feel an obligation to do (sth)   |
|  | observation   | observe   | observationobserver   |    |    | to keep under observationto observe what/how/whereto the casual observer…   |
|  | obtain   | obtain   |    |    |    | to obtain a degreeto be able/unable to obtain   |
|  | obvious   |    |    | obvious   | obviously   | to be obvious (to sb)it is obvious (that)to be obvious froman obvious reason/example/question   |
|  | occasional   |    | occasion   | occasional   | occasionally   | occasion for sb to do sth/occasion for doing sthspecial occasion   |
|  | occupation   | occupy   | occupation   | occupational   |    | an occupational hazard   |
|  | occupy   | occupy   | occupation   | occupied   |    | to be occupied with sth or by sbto occupy a key/prime/major position in sth   |
|  | occur   | occur   | occurrence   |    |    | to occur commonly/frequently/rarely a frequent/rare/common occurrence   |
|  | offense   | offend   | offense   | offensive   |    | criminal/serious/minor offenseto commit an offenseto be offended by/at sthoffensive to (sb)   |
|  | ongoing   |    |    | ongoing   |    | an ongoing project/research   |
|  | operate   | operate   | operation   | operationaloperating   |    | to operate a machine/a businessto have an operationto do/carry out an operation   |
|  | optimistic   | optimismoptimist   |    | optimistic   | optimistically   | to be (extremely/quite/reasonably) optimistic about sth  to be/appear/seem/sound/remain optimistic  an optimistic view/optimistic expectations  to think optimistically   |
|  | option   |    | option   | optional   |    | to have many (or few) options   |
|  | ordinary   |    |    | ordinaryextraordinary   | ordinarilyextraordinarily   | ordinary peoplean ordinary life   |
|  | orient   | orient   | orientation   |    |    | to orient sth in the direction of something elseorientation meeting   |
|  | outcome   |    | outcome   |    |    | to have a negative/positive outcomethe outcome of sth the final/ultimate outcome   |
|  | overseas   |    |    | overseas   |    | overseas travelan overseas bank accountto come from/travel/study overseas   |
|  | paradigm   |    | paradigm   | paradigmatic   |    | to shift/establish/adopt/become a paradigmparadigm shift/example/case   |
|  | participant   | participate   | participationparticipant   |    |    | to participate in sthan active participant/active participation   |
|  | particular   |  |  | particular   | particularly   | of particular interest/concern/importance (to sb/sth)   |
|  | passionate   |    |    | passionate   | passionately   | to be/feel passionate about sthto have a passionate belief/interest in sthto believe passionately in stha passionate speech/personto speak passionately about sth   |
|  | perceive   | perceive   | perception   |    |    | to be commonly/generally/widely perceivedto be perceived as sth   |
|  | permanent   |    |    | permanent   | permanently   | a permanent job/contract /employment/residence a permanent employee/worker/staff/resident a permanent change/damage/solution/arrangementpermanently damaged/banned   |
|  | permission   | permit   | permissionpermit   |    |    | to have/get/receive permission for sthto give sb permissionresidence permit/work permitwithout permission   |
|  | persuade   | persuade   | persuasion   | persuasive   |    | to persuade sb to do sthto persuade sb into doing sthto try/manage/fail to persuade sbpersuasive argument/evidencepersuade sb of sth   |
|  | pessimistic   | pessimismpessimist   |    | pessimistic   | pessimistically   | to be (extremely/quite/too) pessimistic about sthto be/appear/seem/sound/remain pessimistica pessimistic viewto think pessimistically   |
|  | phase   | phase   | phase   |    |    | to phase sth out in/during a period of timephases of the moon   |
|  | phenomenon   |    | phenomenon   | phenomenal   |    | phenomenon of sth   |
|  | philosophy   |    | philosopherphilosophy   | philosophical   | philosophically   | a personal philosophy   a philosophy of sth  to be philosophical about sth  philosophic writings   |
|  | physiological   |    | physiology   | physiological   | physiologically   | a physiological problem/causea physiological reactionthe physiology of the brain   |
|  | policy   |    | policy   |    |    | foreign/economic/public policypolicy on/for sthto adopt/implement new/firm policies   |
|  | polluted   | pollute   | pollution   | pollutedunpolluted   |    | water/air/noise/light pollutionpollution levels/controlpolluted air/water/riversto pollute sth with sth   |
|  | possess   | possess   | possession   | possessive   |    | illegal possessionto gain/get/obtain possession   |
|  | postpone   | postpone   |  |  |  | to postpone sth (until a later time)  to postpone a meeting/an event   |
|  | potential   |    | potential   | potential   | potentially   | to have (great) potential for stha potential customer/buyer/clienta potential danger/threat/risk/benefit/problem   |
|  | poverty   |    | poverty   |    |    | extreme/severe povertyto live in povertyto fight/address/end/escape poverty   |
|  | praise   | praise   | praise   |    |    | praise sb/sth for (doing) sth   |
|  | precise   |    | precision   | precise   | precisely   | to be precise about sthto know preciselyto be precise about sth to know precisely   |
|  | predict   | predict   | prediction   | predictable unpredictable   | predictablyunpredictably   | to predict sth correctly/successfully to make predictions about sthto be predictable a/n accurate/correct prediction   |
|  | presence   |    | presence   | present   |    | (to do sth) in the presence of sbto notice/acknowledge sb’s presenceto indicate/detect the presence of sb/sth   |
|  | preserve   | preserve   | preservation   |    |    | to preserve sth for future generationspreservation of sth (the environment, etc)   |
|  | pressure   |  | pressure   |  |  | to be/come under pressure  (to put) pressure on sb   |
|  | pretend   | pretend   | pretension   |    |    | to pretend (that)to pretend to do/be something   |
|  | prevention   | prevent   | prevention   | preventable   |    | disease/accident/crime preventionto prevent sb from doing sthpreventable diseases/accidents   |
|  | previously   |  |  | previous   | previously   | the previous year/month/week/day/nightprevious experience    |
|  | primary   |    |    | primary   | primarily   | primary purpose/objective/aimprimary reason/cause/function/role   |
|  | primitive   |    |    | primitive   | primitively   | primitive toolsprimitive behavior (negative)   |
|  | prior   | prioritize   | priority   | prior   |    | prior to sthhigh/major/top/immediate/low priority prior knowledge/experience   |
|  | procedure   | proceed   | procedure   |    |    | complex/complicated/simple procedureprocedure for  to follow/establish/adopt a procedure   |
|  | process   | process   | process   | processed   |    | to process data/informationto process an application (or other documents)the production processprocessed food   |
|  | productive   | producereproduce   | (re)productionproductproducer   | productiveunproductive   | productively   | productive land/workers/meetings   |
|  | profit   |    | profit   | profitable   |    | to profit from sth to make a profit to be profitable at a profit/for profit   |
|  | progress   | progress   | progress   | progressive   |    | to achieve/make progresseconomic/scientific progressconsiderable/great/impressive progress   |
|  | prohibit   | prohibit   | prohibition   | prohibitive   |    | to prohibit from sth to impose/lift prohibitions prohibition against/of sth   |
|  | promote   | promote   | promotion   | promotional   |    | to promote sb to sth   |
|  | proof   | prove   | proof   | proven   |    | to prove sth to sbto have proof concrete/absolute/clear proof   |
|  | proportion   |    | proportion   | proportional   |    | a large/small/equal/significant/direct proportion   |
|  | propose   | propose   | proposal   |    |    | to make/put forward/submit a proposal to propose to do sth to propose doing sth to propose a plan/an idea   |
|  | protection   | protect   | protectionprotector   | protectiveprotectedunprotected   | protectively   | to protect sb from/against sthunder protectiongive/offer/provide protection   |
|  | psychologist   |    | psychologypsychologist   | psychological   | psychologically   | clinical/educational/child/sport psychology   |
|  | purchase   | purchase   | purchase   |    |    | to make a purchaseexpensive purchaseproof of purchase   |
|  | pursue   | pursue   | pursuit   |    |    | to pursue a career in sthto pursue an interest/a goal/your ambitionspursuit of happiness   |
|  | qualification   | qualify   | qualification   | qualifiedunqualified   |    | to have/hold/obtain/gain qualification(s)excellent/good/low/poor quality   to be qualified to do sthqualification in/for   |
|  | quit   | quit   |    |    |    | to quit doing sth   |
|  | radical   |    | radical (a person)   | radical   | radically   | radical changes/ideas/solutions   |
|  | raise   | raise   | raise   |  |  | to raise money/funds  to raise awareness about sth  to raise a question/an issue  to raise taxes/salaries/prices   a pay/salary raise    |
|  | random   |    |    | random   | randomly   | a random sample/selection/movement   |
|  | range   | range   | range   |    |    | wide/broad/full/narrow/limited range of sth  to range from sth to sth  to range between sth to sth  to range in size/price/age, etc.   |
|  | rapid   |    | rapidity   | rapid   | rapidly   | a rapid growth/expansion/development/increase/progressincrease/rise/declineat a rapid rate/paceto grow/expand/increase rapidly   |
|  | rare   |    | rareness   | rare   | rarely   | to become/get rareextremely/quite/rather rare   |
|  | ratio   |    | ratio   |    |    | the ratio of a to bratio between   |
|  | reaction   | react   | reaction   |    |    | to react to/against sth/sbto react positively/negatively/appropriately   |
|  | reasonable   | reason   | reason   | reasonable   | reasonably   | the main/major reason for stha reasonable explanation/excusea reasonable question/priceperfectly/entirely reasonable   |
|  | recall   | recall   |    |    |    | to recall doing sth   |
|  | recognition   | recognize   | recognition   |  |  | recognition of sth/sbto have/give/receive formal/official recognitionfacial recognition   |
|  | recommend   | recommend   | recommendation   |    |    | on sb’s recommendationto give/make a recommendation to sb   |
|  | recover   | recover   | recovery   |    |    | to recover completely/fully/partially to make a recovery from sth amazing/full/fast/slow recovery   |
|  | reduction   | reduce   | reduction   |    |    | a reduction in/of stha reduction in the number of stha significant/dramatic/gradual/slight reductionto make/get a reduction on sthto reduce sth/the risk of sthto reduce sth by ..%   |
|  | refer   | refer   |  |  |  | to refer to sb/sth (as sb/sth)  to refer to data/statistics/ a book/document/an article   |
|  | refuse   | refuse   | refusal   |    |    | to refuse a(n) request/visa/invitation/offer   |
|  | regard   | regard   | regard   | regardlessregarding (preposition)   |    | regardless of sthto regard sth as sthregard forwith/in regard to sth   |
|  | register   | register   | registration   | registered   |    | to register to vote to register for classes   |
|  | regulate   | regulate   | regulation   | regulatory   |    | strict/tight/poor/weak regulation to regulate carefully/closely   |
|  | regulation   | regulate   | regulation   | regulatory   |    | to regulate drugs or medicines   strict/tight regulationsgovernment/school regulations   |
|  | reinforce   | reinforce   | reinforcement   |    |    | to reinforce a belief   to reinforce with/by sthpositive reinforcement   |
|  | reject   | reject   | rejection   |    |    | to reject sb/sth rejection of sth   |
|  | related   | relate   | relation   | related   |    | related toin relation to   |
|  | release   | release   | release   |    |    | to release quickly/eventually/accidentally   early release from prison   |
|  | relevance   |    | relevanceirrelevance   | relevantirrelevant   |    | to be (ir)relevant to sthto seem/become/consider sth relevant/irrelevant   |
|  | reliable   | rely on   | reliance   | reliable   |    | a reliable sourcereliable data/estimate/evidence/figures   |
|  | relief   | relieve   | relief   |    |    | a great/enormous/tremendous reliefa sense/feeling of reliefto provide relief from sthto relieve sth (anxiety/guilt/stress/pain/tension    |
|  | reluctant   |    | reluctance   | reluctant   | reluctantly   | to be reluctant to do sth great/deep/extreme reluctanceto reluctantly agree to/accept sth   |
|  | rely   | rely on   | reliance   | reliableunreliable   |    | to rely on sb/sth to do sthreliance on sb/stha reliable source   |
|  | remain   | remain   | remain   | remaining   |    | to remain in bedto remain silent   |
|  | remedy   |  | remedy   | remediable  remedial   |  | remedy for stha cold/cough/flu remedy   |
|  | remind   | remind   | reminder   |    |    | to remind sb to do sthto remind sb of something/someone   |
|  | remote   |    |    | remote   | remotely   | remote fromto get remote access to sth   |
|  | renewable   | renew   | renewal   | renewable   |  | renewable energy/resources  the renewal of sth   to renew a(n) contract/agreement/passport/subscription  to renew membership (of sth)   |
|  | replacement   | replace   | replacement   | replaceable irreplaceable   |    | a replacement for sth/sb to replace sth/sb with sth/sb   |
|  | representative   | represent   | representationrepresentative   | representative   |    | to represent a change/an advance/an increaseto represent sb/sth as sth   |
|  | reputation   |  | reputation   | reputational   |  | earn/establish/gain/acquire a reputation (as.. sth/sb)the reputation ofto enhance/damage sb’s reputation   |
|  | require   | require   | requirement   |    |    | course/visa/safety/entrance requirementsto meet the requirements   |
|  | rescue   | rescue   | rescue   |  |  | a rescue team  to rescue sb/sth from sb/sth  a rescue attempt/effort   |
|  | resemble   | resemble   | resemblance   |    |    | to closely resemble sth/sb a close/strong resemblance (between sth/sb and sth/sb)   |
|  | resident   |    | residenceresident   | residential   |    | a residential property/area/neighborhooda permanent resident /residence   |
|  | resistant   | resist   | resistance   | resistant   |    | resistance to/fromto put up/offer resistancewind/air/water resistanceto resist the urge/a trend/a tendency   |
|  | resolve   | resolve   | resolution   |    |    | to resolve a problem/an issueto make/keep a resolution   |
|  | resource   |    | resource   | resourceful   |    | the distribution of resourcesfinancial/natural/limited resources   |
|  | respond   | respond   | response   | responsive   |    | to respond quickly/effectively   to respond to sth   |
|  | restore   | restore   | restoration   |    |    | to restore a building/antiquesto restore sb’s faith in sthto be closed for restoration   |
|  | restriction   | restrict   | restriction   | restrictedrestrictive   |    | to restrict sb’s behavior   to restrict seriously/unnecessarily   |
|  | retain   | retain   |    |    |    | to retain control of sth   |
|  | reveal   | reveal   | revelation   |    |    | to reveal sb as/to be sth revelation of sth   |
|  | revenue   |    | revenue   |    |    | estimated revenue   |
|  | revolution   | revolutionize   | revolution   | revolutionary   |    | social/cultural revolution   |
|  | reward   | reward   | reward   | rewarding   |    | to reward sb with sthto reward sb for (doing) sthto get/receive one’s rewarda financially rewarding career   |
|  | sample   | sample   | sample   |    |    | to take/collect/give/provide/analyze/test a samplea blood/tissue/ DNA sample   |
|  | satisfaction   | satisfy   | satisfaction   | satisfactoryunsatisfactory   | satisfactorilyunsatisfactorily   | to satisfy a need   |
|  | secure   | secure   | security   | secureinsecure   | securely   | job securityeconomically secureto secure a deal/contract/place   |
|  | sedentary   |    |    | sedentary   |    | a sedentary life/ job/occupation/lifestyle   |
|  | selection   | select   | selection   | selectiveselected   | selectively   | to make selection to be very/extremely selective   |
|  | sense   | sense   | sense   | sensible   | sensibly   | a sense of achievement/satisfaction/responsibility/dutythe sensible thing to doto appear sensible   |
|  | separate   | separate   | separation   | separate   | separately   | to separate sth from sthto keep sth separate from sth   |
|  | settlement   | settle   | settlement   |    |    | to reach a legal settlementto settle insettlement of   |
|  | severe   |    | severity   | severe   | severely   | severe damagesevere problems/difficultiesa severe injury/illness/pain   |
|  | shortage   |    | shortage   |    |    | to create/cause a shortage a water/food/housing shortage   |
|  | signal   |  | signal  sign   |  |  | a signal for sth  (to give) sb a signal to do sth  a clear sign of sth   |
|  | significant   |    | significance   | significantinsignificant   | significantly   | to be significant to or for sth/sbto attach significance to   |
|  | similarity   |    | similarity   | similar   | similarly   | to be similar to sb/stha (striking) similarity between (two people or two objects)   |
|  | slight   |    |    | slight   | slightly   | a slight increase/change/difference/improvementto increase/decrease slightly   |
|  | solely   |    |    | sole   | solely   | to do sth solely for the moneyto be solely responsible   |
|  | sophisticated   |    | sophistication   | sophisticated   |    | highly sophisticated   |
|  | source   | source   | source   |    |    | source of income/source of pride   |
|  | specialize    | specialize   | specialist   | specialized   |  | to specialize in sth  to specialize in a subject/area/field  specialized training/skills  to be highly specialized   |
|  | species   |    | species   |    |    | human/extinct species   |
|  | specific   | specify   | specification   | specific   | specifically   | to be specific (about sth)a specific time/place   |
|  | spread   | spread   | spread   |    |    | to limit/control the spread ofto spread to/through/over/among sthto spread (from sth) to sth   |
|  | stability   | stabilize   | stability   | stableunstable   |    | a stable job/stable prices  to remain stable   |
|  | steadily   |    |    | steady   | steadily   | to remain steady   |
|  | stimulation   | stimulate   | stimulation   | stimulating   |    | to stimulate growth/demand/the economy a stimulating effect/environment   |
|  | strengthen   | strengthen   | strength   | strong   | strongly   | to strengthen sth’s ties/bonds/linksto strengthen a relationshipto have/find the strength to do sthmental/inner strengthstrong feelings/views/opinions/support/oppositionto strongly advise/encourage   |
|  | stress   | stress=emphasize   | stress   | stressfulstressed   | stressfully   | to stress the importance of sthto stress the need for stha stressful time/situation/lifeto be/feel stressed   |
|  | strictly   |    | strictness   | strict   | strictly   | to be treated strictly to be strictly controlledstrict about/with   |
|  | structure   | structure   | structure   | structural   |    | social/political/economic structure molecular structure   |
|  | struggle   | struggle   | struggle   |    |    | to struggle to do sthto struggle with/for/against sthto face a struggle   |
|  | submit   | submit   | submission   |    |    | to submit an application/claim/proposal/assignmentto submit one’s resignation   |
|  | substantial   |    |    | substantial   | substantially   | substantial decrease/increase   |
|  | suburb   |    | suburb   | suburban   |    | to live/grow up in the suburbsa suburb of a town/city/metropolis a wealthy /poor suburba suburban community   |
|  | suffer   | suffer   | suffering   |    |    | to suffer from an illness   |
|  | sufficient   |    |    | sufficient insufficient   | sufficiently insufficiently   | sufficient to do sthsufficient for sth   |
|  | summarize   | summarize   | sumsummary   |    |    | to summarize the main pointsa summary of sth   |
|  | supplement   | supplement   | supplement   | supplemental supplementary   |    | supplemental income   dietary supplementsto supplement sth by/with stha supplementary material   |
|  | supply   | supply   | supply   |    |    | a food/water/money supplyan endless supply of sth   |
|  | surface   |  | surface   |  |  | beneath/under/below the surface  on the surface  to rise to the surface   |
|  | surgery   |    | surgerysurgeon   |    |    | to have/undergo/perform/carry out surgery (on sth)to need/require surgerycosmetic/plastic/emergency surgery   |
|  | survey   | survey   | survey   |    |    | to carry out/conduct a survey   the findings/results of a surveya recent/new survey   |
|  | survive   | survive   | survival  survivor   | survival   |    | to survive sth  a survival instinct  survival skills/strategies   |
|  | suspect   | suspect   | suspect  suspicion   | suspicious   | suspiciously   | to be suspected of sth  to suspect sb of (doing) sth  to question/interview a suspect  to be suspicious of sth/sb  to act/behave suspiciously   |
|  | sustainable   | sustain   | sustainability   | sustainable   |    | sustainable energy sourcesenvironmentally sustainable   |
|  | symptom   |    | symptom   | symptomatic   |    | to display a symptom symptoms of a disease   |
|  | target   | target   | target   |    |    | to reach/achieve/hit a target to meet a targetachievable/realistic target   |
|  | technique   |    | technique   | technical   | technically   | to use/have a techniqueeffective/successful/simple technique to be very/extremely technical   |
|  | temporary   |    |    | temporary   | temporarily   | on a temporary basistemporary measure   |
|  | tend   | tend   | tendency   |    |    | to tend to do sth to have a tendency to do sth   |
|  | terrifying    | terrify   |  | terrifying  terrified   |  | terrified of sth  a terrifying experience/encounter   |
|  | theme   |    | theme   | thematic   | thematically   | a thematic arrangement/to be thematically arrangedthe main/central/major theme of a book/film/playa familiar/common theme   |
|  | threat   | threaten   | threat   | threatening   |    | to pose a threata threat against sth   |
|  | tough   |    |    | tough   |    | to be tough on/with somebodytough choice/decision/call/question   |
|  | trace   | trace   | trace   |  |  | to trace the origin/history of sth(to disappear/leave) without a trace   |
|  | trait   |  | trait   |  |  | personality/character traitsgenetic/inherited traits   |
|  | transform   | transform   | transformation   |    |    | to undergo a dramatic/amazing transformation   |
|  | treat   | treat   | treatment   | treatable   |    | emergency/long-term/dental/medical treatmentto have/require/receive/undergo treatmentto give sb treatmenta treatment methodto be in treatment for   |
|  | trigger   | trigger   | trigger   |    |    | to trigger a memory/a response/the alarm   |
|  | ultimately   |    |    | ultimate   | ultimately   | the ultimate aim   |
|  | underestimate   | underestimate overestimate estimate   | underestimation overestimationestimate   |    |    | to underestimate sb or sb’s abilities to underestimate the importance/effect/power of sth difficult/hard to estimate sth to make an estimate of sth   |
|  | undergo   | undergo   |    |    |    | to undergo a development process   |
|  | undertake   | undertake   |    |    |    | to undertake a task/a project/a study/a responsibilityto undertake research   |
|  | unfamiliar   |  |  | unfamiliar  familiar   |  | (un)familiar to sb  to be unfamiliar with sb/sth  an unfamiliar environment   to seem/sound unfamiliar   |
|  | unique   |    | uniqueness   | unique   | uniquely   | a unique opportunity to be unique to sb/sth   |
|  | universal   |  |  | universal   | universally   | universal access/standards/health care   |
|  | unjustly   |    |    | unjust   | unjustly   | to be unjustly accused of sthunjust law/decision   |
|  | unpredictable   | predict   | prediction   | predictableunpredictable   |    | to predict sth correctly/successfully to make predictions about sth to be (un)predictable   |
|  | upgraded   | upgrade   | upgrade   | upgraded   |    | an upgraded version of sth   |
|  | urban   |  |  | urban   |  | urban areas/peopleurban development   |
|  | urge   | urge   | urge   |    |    | to urge sb to do sth   |
|  | valid   |    | validity   | valid  invalid   |    | (in)valid reasons  a valid claim/argument   |
|  | value   | valueovervalueundervalue   | value   | valuableinvaluable   |    | good/poor valueto fall/increase in valuestreet/market valuevaluable information/time/help   to value sb/sth for sth   |
|  | variable   | vary   | variation variety   | variablevariousvarying   |    | to vary from sth to sthto give/add/bring variety to stha variety of sthvarying types of sth variation of/in/among/betweento vary greatly/slightly/considerably/enormously   |
|  | vast   |  |  | vast   | vastly   | a vast majority/ amount of sth/sb   |
|  | virtual   |    |    | virtual   | virtually   | virtual reality   |
|  | visible   |    | visibility   | visibleinvisible   | visiblyinvisibly   | to be (in)visible to sb   |
|  | visual   | visualize   | visualization   | visual   |    | to visualize sth   |
|  | vital   |    |    | vital   | vitally   | to be vital for sb/sthto play a vital role of vital importance in sth   |
|  | volunteer   | volunteer   | volunteer   | voluntaryinvoluntary   | voluntarilyinvoluntarily   | to volunteer to do sthto volunteer for sthto do sth voluntarilyvoluntary work/servicea voluntary organization/association/agency   |
|  | wage   |    | wage   |    |    | the minimum wage to earn/pay wages   |
|  | wealth   |    | wealth   | wealthy   |    | personal wealthenormous/considerable wealthto create/accumulate/acquire wealth   |
|  | widely   |  |  |  | widely   | widely known/adapted/ believed    |
|  | widespread   |    |    | widespread   |    | widespread damage/support   |
|  | willing   | will   | willingnesswill   | willingunwilling   | willinglyunwillingly   | to show/express willingness   to be (un)willing to do sth to (un)willingly accept sththe will to live/fight/succeedat will   |
|  | witness   | witness   | witness   |    |    | to witness an accident/a murder/an attackto have a witness to sth   |
|  | worth   | worth   | worth   | worthyunworthyworthless   |    | worth doing sthto be worthy of sth   |
"""

unit_data = """
| UNIT 1: READING & WRITING  <td colspan=7/> |
| appreciation | appreciate | appreciation | | | to appreciate the importance/value of sth, to deeply appreciate, show appreciation |
| bond | bond | bond bonding | | | to form a bond with, bond between A and B, a close/strong/special bond |
| capable | | capability | capable incapable | | to be capable of sth, have capability |
| challenge | challenge | challenge | challenging | | significant challenge, to challenge sb/sth |
| complex | | complexity | complex | | a highly complex system, complexity of a situation |
| consciousness | | consciousness | conscious | consciously | conscious of doing sth |
| demonstrate | demonstrate | demonstration | | | demonstrate how/what/why |
| domesticate | domesticate | domestication | domestic | domestically | domesticate an animal, domestic flights |
| establish | establish | establishment | | | establish a company, establish relations with |
| extended | extend | extension | extended | | extend a deadline, extended family |
| evidence | | evidence | | | evidence for/of/against sth |
| evolve | evolve | evolution | evolutionary | | evolve from/into sth |
| hierarchy | | hierarchy | hierarchical | hierarchically | social hierarchy |
| intense | | | intense | intensely | intense feelings, intense pressure |
| notion | | notion | | | have a notion about sth |
| observe | observe | observation observer | | | keep under observation |
| previously | | | previous | previously | previous year, previous experience |
| primary | | | primary | primarily | primary purpose, primary reason |
| recognition | recognize | recognition | | | recognition of sth, receive official recognition |
| replace | replace | replacement | replaceable irreplaceable | | replacement for sth, replace A with B |
| similarity | | similarity | similar | similarly | striking similarity between |
| species | | species | | | human species, extinct species |
| strict | | strictness | strict | strictly | strictly controlled, strict with |
| structure | structure | structure | structural | | social structure, economic structure |
| suffering | suffer | suffering | | | suffer from an illness |
| treat | treat | treatment | treatable | | undergo treatment, treatment method |
| visible | | visibility | visible invisible | visibly invisibly | visible to sb |
| worth | worth | worth | worthy worthless | | worth doing sth, worthy of sth |

| UNIT 1: LISTENING & SPEAKING  <td colspan=7/> |
| actual | | | actual | actually | in actual fact |
| approximately | | | approximate | approximately | approximate amount |
| assume | assume | assumption | | | make assumptions about, common assumption |
| aware | | awareness | aware unaware | | raise awareness, aware of sth |
| bargain | bargain | bargain | | | make a bargain, bargain with sb |
| commercial | commerce | commercial | commercial | commercially | commercial transaction, global commerce |
| competition | compete | competition competitor | competitive | competitively | in competition with, compete against |
| concerned | concern | | concerned | | concerned with |
| consumer | consume | consumer consumption | consumer | | consumer rights, boost consumption |
| convenient | | convenience | convenient inconvenient | conveniently | highly convenient |
| credit | | credit | | | get the credit, buy on credit |
| declare | declare | declaration | | | declare victory/bankruptcy |
| debt | | debt | | | deeply in debt to, pay off debt |
| essential | | | essential | essentially | essential to/for sth |
| estimate | estimate | estimate estimation | | | estimate of costs, make an estimate |
| extent | | extent | | | extent of sth, to a large extent |
| fascinating | | | fascinating fascinated | | fascinating discovery |
| influence | influence | influence | influential | | under the influence of, have influence on |
| interrupt | interrupt | interruption | | | without interruptions |
| productive | produce reproduce | production product | productive | productively | productive meetings, productive land |
| psychology | | psychology psychologist | psychological | psychologically | psychological well-being |
| purchase | purchase | purchase | | | make a purchase, proof of purchase |
| react | react | reaction | | | react to sth, react positively |
| shortage | | shortage | | | water/housing shortage |
| wealthy | | wealth | wealthy | | personal wealth, accumulate wealth |

| UNIT 1: EXTRA WORDS  <td colspan=7/> |
| concrete | | | concrete | | concrete proposal/proof |
| deviate | deviate | deviation | | | deviate from sth |
| dilemma | | dilemma | | | dilemma about/over, in a dilemma |
| disrupt | disrupt | disruption | disruptive | | disrupted by sth, cause disruption |
| expense | | expense | expensive | expensively | living expense, additional expense |
| framework | | framework | | | organizational framework |
| inferior | | | inferior | | feel inferior to sb |
| occupation | occupy | occupation | occupational | | occupational hazard |
| pretend | pretend | | | | pretend to do sth |
| theme | | theme | thematic | thematically | central theme of |

| UNIT 2: READING & WRITING  <td colspan=7/> |
| admit | admit | admission | | | admit openly, admission of guilt |
| advance | advance | advancement | advanced | | major advance, advanced technology |
| analysis | analyze | analysis | | | analyze data, conduct an analysis |
| appearance | appear disappear | appearance | | | make an appearance |
| arrest | arrest | arrest | | | arrest sb, under arrest |
| attach | attach | attachment | attached | | develop attachment |
| charge | charge | charge | | | charge sb with a crime, in charge of |
| combination | combine | combination | | | combination of factors |
| commit | commit | commitment | committed | | commit a crime, make a commitment |
| consider | consider reconsider | consideration | | | take into consideration |
| detect | detect | detection detective | | | detect illnesses |
| determine | determine | determination | determined | | show determination |
| examine | examine | examination | | | examine closely, under examination |
| extract | extract | extract extraction | | | extract data from, extraction of minerals |
| feature | feature | feature | | | key features of sth |
| identity | identify | identity | identified | | identify sb, identity card |
| method | | methodology | methodological | methodologically | scientific methodology |
| presence | | presence | present | | in the presence of |
| proportion | | proportion | proportional | | significant proportion |
| prove | prove | proof | proven | | prove sth, concrete proof |
| reveal | reveal | | | | reveal sth to sb |
| specialize | specialize | specialist | specialized | | specialize in sth |
| suspect | suspect | suspect suspicion | suspicious | suspiciously | suspect sb of doing sth |
| technique | | technique | technical | technically | effective technique |
| trace | trace | trace | | | trace the origin of, without a trace |
| witness | witness | witness | | | witness an accident |

| UNIT 2: LISTENING & SPEAKING  <td colspan=7/> |
| adapt | adapt | adaptation | adaptable | | adapt to sth, adaptable |
| affect | affect | effect | effective ineffective | effectively | affect sth, have an effect on |
| circumstance | | circumstance | | | under certain circumstances |
| classical | | | classical classic | classically | classic example, classical music |
| conclude | conclude | conclusion | conclusive | | in conclusion, conclusive evidence |
| controversial | | controversy | controversial | controversially | highly controversial |
| criticism | criticize | criticism | critical | critically | criticize sb for, critical comment |
| decade | | decade | | | decades-long |
| dishonest | | dishonesty | dishonest | | dishonest way |
| eliminate | eliminate | elimination | | | eliminate sth from |
| exposed | expose | exposure | exposed | | exposed to sth, massive exposure |
| extreme | | | extreme | extremely | extreme conditions, extreme poverty |
| evaluate | evaluate | evaluation | evaluative | | evaluate performance |
| generation | | generation | | | younger generation, generation gap |
| identical | | | identical | identically | identical twins |
| illegal | | | legal illegal | legally illegally | legal action |
| investigate | investigate | investigation investigator | | | investigate closely, under investigation |
| manual | | | manual | manually | manual labor |
| mode | | mode | | | mode of transportation |
| precise | | precision | precise | precisely | precise about, know precisely |
| refuse | refuse | refusal | | | refuse a request |
| reject | reject | rejection | | | reject an offer |
| sample | sample | sample | | | collect a sample, blood sample |
| specific | specify | specification | specific | specifically | specific time/place |
| trait | | trait | | | personality traits, genetic traits |
| unique | | uniqueness | unique | uniquely | unique opportunity |

| UNIT 2: EXTRA WORDS  <td colspan=7/> |
| accuse | accuse | accusation | accusing accused | | accuse sb of doing sth |
| alter | alter | alteration | | | alter perceptions, make alterations |
| blend | blend | blend | | | blend A with B |
| hypothesize | hypothesize | hypothesis | hypothetical | hypothetically | hypothetical situation |
| incident | | incident | | | without incident, incident occurs |
| innocence | | innocence | innocent | | innocent people |
| justify | justify | justice justification | justified unjust | | justify doing sth |
| moral | | morality | moral immoral | morally | moral dilemma, morally right |
| paradigm | | paradigm | paradigmatic | | paradigm shift |
| summarize | summarize | summary | | | summarize main points |

| UNIT 3: READING & WRITING  <td colspan=7/> |
| aspect | | aspect | | | key aspect of sth |
| barrier | | barrier | | | overcome barriers |
| concentration | concentrate | concentration | concentrated | | high concentration of |
| construction | construct | construction | constructive | | constructive criticism |
| conventional | | | conventional | conventionally | conventional behavior |
| growth | grow | growth | | | population growth |
| income | | income | | | annual income |
| inevitable | | inevitability | inevitable | inevitably | inevitable consequence |
| lower | lower | | | | lower costs/prices |
| occasional | | occasion | occasional | occasionally | on occasional basis |
| operate | operate | operation | operational | | operate a business |
| productive | produce | product production | productive | productively | productive work |
| rapid | | rapidity | rapid | rapidly | rapid growth |
| require | require | requirement | | | meet requirements |
| resident | | residence resident | residential | | permanent resident |
| reward | reward | reward | rewarding | | reward sb for, rewarding career |
| separate | separate | separation | separate | separately | separate A from B |
| struggle | struggle | struggle | | | struggle to do sth |
| suburb | | suburb | suburban | | live in the suburbs |
| temporarily | | | temporary | temporarily | on a temporary basis |
| tend | tend | tendency | | | tend to do sth, have a tendency |
| urban | | | urban | | urban development |
| value | value | value | valuable invaluable | | valuable help, value sb for |
| volunteer | volunteer | volunteer | voluntary | voluntarily | voluntary service |
| wage | | wage | | | minimum wage |
| widespread | | | widespread | | widespread support |

| UNIT 3: LISTENING & SPEAKING  <td colspan=7/> |
| acknowledge | acknowledge | acknowledgement | | | acknowledge mistakes |
| agriculture | | agriculture | agricultural | | agricultural sector |
| annual | | | annual | annually | annual report/budget |
| category | categorize | category | categorical | categorically | categorize things |
| citizen | | citizen | | | become a citizen |
| conflict | | conflict | conflicting | | conflict of interests |
| dependent | depend | dependency dependence | dependent independent | independently | depend on, dependent on |
| disaster | | disaster | disastrous | | natural disaster |
| education | educate | education educator | educated educational | | private/public education |
| establish | establish | establishment | | | establish links with |
| ignore | ignore | ignorance | ignorant | | ignorant of |
| illustrate | illustrate | illustration | | | perfect illustration of |
| institute | | institution institute | institutional | | educational institution |
| invest | invest | investment investor | | | invest in sth, sound investment |
| lack | lack | lack | | | lack of resources |
| overseas | | | overseas | | overseas travel |
| permanently | | | permanent | permanently | permanent job, permanently damaged |
| permission | permit | permission permit | | | without permission |
| potential | | potential | potential | potentially | potential risk/benefit |
| poverty | | poverty | | | live in poverty, end poverty |
| refer | refer | | | | refer to sb/sth as |
| settle | settle | settlement | | | settle in, reach a settlement |
| spread | spread | spread | | | limit the spread of |
| supply | supply | supply | | | water supply, endless supply |

| UNIT 3: EXTRA WORDS  <td colspan=7/> |
| achievement | achieve | achievement | | | achieve success |
| brief | | | brief | briefly | fairly brief |
| exceed | exceed | excess | excess | | exceed expectations |
| import | import | import | | | import from, agricultural imports |
| negotiate | negotiate | negotiation | | | negotiate a deal |
| obey | obey | obedience | obedient disobedient | obediently | obey rules |
| orient | orient | orientation | | | orient in the direction of |
| resistant | resist | resistance | resistant | | resistance to, resist the urge |
| revenue | | revenue | | | estimated revenue |
| solely | | | sole | solely | solely responsible |

| UNIT 4: READING & WRITING  <td colspan=7/> |
| affordable | afford | | affordable | | affordable housing |
| collapse | collapse | collapse | | | danger of collapse |
| consequence | | consequence | consequent | consequently | face consequences, as a consequence of |
| demonstration | demonstrate | demonstration | | | demonstrate against |
| destruction | destroy | destruction | destructive | | habitat destruction |
| effectively | affect | effect | effective ineffective | effectively | beneficial effect on |
| entire | | entirety | entire | entirely | in its entirety |
| eventually | | | eventual | eventually | eventual outcome |
| external | | | external | externally | external factors |
| extinction | | extinction | extinct | | extinct species, in danger of extinction |
| failure | fail | failure | | | complete failure |
| forecast | forecast | forecast | | | weather forecast |
| gain | gain | gain | | | gain control, economic gain |
| occur | occur | occurrence | | | common occurrence |
| prediction | predict | prediction | predictable unpredictable | | accurate prediction |
| prior | prioritize | priority | prior | | prior to, prior knowledge |
| rely | rely on | reliance | reliable unreliable | | rely on sb, reliable source |
| severe | | severity | severe | severely | severe damage |
| stable | stabilize | stability | stable | | stable prices |
| steadily | | | steady | steadily | remain steady |
| stress | stress | stress | stressful stressed | stressfully | stress the importance of |
| vast | | | vast | vastly | vast majority |
| threaten | threaten | threat | threatening | | pose a threat against |
| trigger | trigger | trigger | | | trigger a response |

| UNIT 4: LISTENING & SPEAKING  <td colspan=7/> |
| accommodation | accommodate | accommodation | | | provide accommodation |
| apparently | | | apparent | apparently | become apparent |
| appreciate | appreciate | appreciation | | | deeply appreciate |
| appropriate | | appropriateness | appropriate inappropriate | appropriately | appropriate behavior |
| consultant | consult | consultant consultancy | | | consultancy firm |
| dramatic | | | dramatic | dramatically | dramatic impact |
| facilitate | facilitate | facilitator | | | facilitate discussion |
| flow | | flow | | | go with the flow |
| harm | harm | harm | harmful harmless | | harmful effect on |
| impact | impact | impact | impactful | | have an impact on |
| landscape | | landscape | | | urban landscape |
| layer | | layer | | | layer upon layer |
| phenomenon | | phenomenon | phenomenal | | phenomenon of |
| preserve | preserve | preservation | | | preserve for future generations |
| pressure | | pressure | | | under pressure |
| rare | | rareness | rare | rarely | extremely rare |
| remind | remind | reminder | | | remind sb of |
| rescue | rescue | rescue | | | rescue team, rescue attempt |
| slight | | | slight | slightly | slight increase |
| surface | | surface | | | beneath the surface |

| UNIT 4: EXTRA WORDS  <td colspan=7/> |
| compile | compile | compilation | | | compile data |
| dismiss | dismiss | dismissal | | | dismiss an idea |
| distribute | distribute redistribute | distribution redistribution | | | distribute equally |
| funding | fund | funding | funding | | research funding |
| grant | grant | grant | | | government grant |
| incentive | | incentive | | | financial incentive |
| insert | insert | insertion | | | insert sth into |
| prevention | prevent | prevention | preventable | | disease prevention |
| radical | | radical | radical | radically | radical changes |
| random | | | random | randomly | random sample |

| UNIT 5: READING & WRITING  <td colspan=7/> |
| alternative | | alternative | alternative | alternatively | alternative to sth |
| assess | assess | assessment | | | assess performance |
| attraction | attract | attraction | attractive | attractively | attract attention |
| award | award | award | | | receive an award |
| awareness | | awareness | aware unaware | | raise awareness of |
| benefit | benefit | benefit | beneficial | beneficially | benefit from, beneficial to |
| define | define | definition | | | defined as |
| diverse | | diversity | diverse | | wide diversity |
| economy | | economy economics | economic economical | economically | economic crisis |
| enhance | enhance | enhancement | | | enhance performance/skills |
| innovative | innovate | innovation innovator | innovative | | innovative ideas |
| insight | | insight | | | insight into |
| livelihood | | livelihood | | | earn a livelihood |
| maintain | maintain | maintenance | | | maintain a building |
| objective | | objective | | | primary objective |
| policy | | policy | | | economic policy |
| renewable | renew | renewal | renewable | | renewable energy |
| sustainable | sustain | sustainability | sustainable | | sustainable energy |
| vital | | | vital | vitally | vital role |

| UNIT 5: LISTENING & SPEAKING  <td colspan=7/> |
| administer | administer | administration | administrative | | administer tests |
| approach | approach | approach | | | new approach to |
| bias | bias | bias | biased | | bias against |
| clarify | clarify | clarification | | | clarify expectations |
| commission | | commission | | | human rights commission |
| criticize | criticize | criticism | critical | critically | criticize sb for |
| determine | determine | determination | determined | | strong determination |
| dominate | dominate | dominance | dominant | | dominant role |
| entire | | entirety | entire | entirely | entire life |
| executive | | executive | | | senior executive |
| exist | exist | existence | existing | | bring into existence |
| feedback | | feedback | | | positive feedback |
| finance | finance | finance | financial | financially | financial advisor |
| gradually | | | gradual | gradually | gradual increase |
| interact | interact | interaction | interactive | interactively | interact with |
| numerous | | | numerous | | numerous studies |
| participate | participate | participation participant | | | participate in |
| profit | | profit | profitable | | make a profit |
| promote | promote | promotion | promotional | | promote sb to |
| qualify | qualify | qualification | qualified unqualified | | qualified to do |
| reputation | | reputation | reputational | | establish a reputation |
| strengthen | strengthen | strength | strong | strongly | strengthen bonds |
| willing | will | willingness | willing unwilling | willingly | willing to do sth |

| UNIT 5: EXTRA WORDS  <td colspan=7/> |
| adequate | | | adequate inadequate | adequately | adequate for |
| attribute | attribute | attribution | | | attribute sth to |
| fulfillment | fulfil | fulfillment | fulfilled | | fulfil ambition |
| implement | implement | implementation | | | implement changes |
| incorporate | incorporate | incorporation | | | incorporate into |
| occupy | occupy | occupation | occupied | | occupy a position |
| pursue | pursue | pursuit | | | pursue a career |
| reluctant | | reluctance | reluctant | reluctantly | reluctant to accept |
| selection | select | selection | selective | selectively | highly selective |

| UNIT 6: READING & WRITING  <td colspan=7/> |
| associate | associate | association | associated | | associated with |
| autonomous | | autonomy | autonomous | autonomously | autonomous learners |
| availability | | availability | available unavailable | | availability of |
| conduct | conduct | conduct | | | conduct a survey |
| contribute | contribute | contribution | | | contribute to, make a contribution to |
| distinguish | distinguish | | distinguished | | distinguish A from B |
| effective | affect | effect | effective | effectively | effective solution |
| ensure | ensure | | | | ensure safety |
| ethnicity | | ethnicity | ethnic | ethnically | ethnic diversity |
| flexible | | flexibility | flexible inflexible | | flexible about |
| initially | | | initial | initially | initial impression |
| minor | | | minor | | minor injury |
| logical | | logic | logical illogical | logically | logical conclusion |
| obtain | obtain | | | | obtain a degree |
| obvious | | | obvious | obviously | obvious reason |
| postpone | postpone | | | | postpone a meeting |
| praise | praise | praise | | | praise sb for |
| register | register | registration | registered | | register for classes |
| remote | | | remote | remotely | remote access |
| resemble | resemble | resemblance | | | resemble closely |
| resolve | resolve | resolution | | | resolve a problem |
| respond | respond | response | responsive | | respond quickly |
| signal | | signal | | | clear signal |
| ultimately | | | ultimate | ultimately | ultimate aim |
| variety | vary | variety variation | various | | variety of |
| visual | visualize | visualization | visual | | visualize sth |

| UNIT 6: LISTENING & SPEAKING  <td colspan=7/> |
| absence | | absence | absent | | in the absence of |
| adjustment | adjust | adjustment | adjustable | | adjust to, make an adjustment |
| apply | apply | application | | | apply for a job, apply to |
| assignment | assign | assignment | | | homework assignment |
| committed | commit | commitment | committed | | committed to |
| component | | component | | | key component |
| concept | | concept | conceptual | | concept of |
| critical | criticize | criticism | critical | critically | critical thinking |
| crucial | | | crucial | crucially | crucial role |
| display | display | display | | | on display |
| enable | enable | | | | enable sb to do |
| encounter | encounter | encounter | | | encounter a problem |
| exhibition | exhibit | exhibition | | | exhibit artwork |
| function | function | function | functional | | perform a function |
| imply | imply | implication | | | implications of |
| philosophy | | philosophy philosopher | philosophical | philosophically | personal philosophy |
| pollute | pollute | pollution | polluted | | air/water pollution |
| priority | prioritize | priority | prior | | top priority |
| satisfaction | satisfy | satisfaction | satisfactory | satisfactorily | satisfy a need |
| unfamiliar | | | unfamiliar familiar | | unfamiliar environment |

| UNIT 6: EXTRA WORDS  <td colspan=7/> |
| abstract | | | abstract | | abstract concept |
| blame | blame | blame | | | blame sb for |
| contemporary | | contemporary | contemporary | | contemporary society |
| imitate | imitate | imitation | | | imitate sb |
| initiative | initiate | initiative | | | launch an initiative |
| irony | | irony | ironic | ironically | cruel irony |
| phase | phase | phase | | | phase out |
| prohibit | prohibit | prohibition | prohibitive | | prohibit from |
| retain | retain | | | | retain control of |

| UNIT 7: READING & WRITING  <td colspan=7/> |
| attitude | | attitude | | | positive attitude towards |
| capacity | | capacity incapacity | | | operate at full capacity |
| convert | convert | conversion | convertible | | convert to |
| currently | | | current | currently | current situation |
| efficient | | efficiency | efficient inefficient | efficiently | energy-efficient |
| generate | generate | generation | | | generate revenue/ideas |
| global | | globe | global | globally | global reach |
| install | install | installation | | | install an app |
| launch | launch | launch | | | launch a campaign |
| regulate | regulate | regulation | regulatory | | strict regulation |
| related | relate | relation | related | | related to |
| relevant | | relevance irrelevance | relevant irrelevant | | relevant to |
| restrictive | restrict | restriction | restrictive | | restrict behavior |
| submit | submit | submission | | | submit an application |
| survey | survey | survey | | | conduct a survey |
| threat | threaten | threat | threatening | | pose a threat |

| UNIT 7: LISTENING & SPEAKING  <td colspan=7/> |
| bother | bother | bother | | | bother to do |
| conservation | | conservation | | | environmental conservation |
| consistent | | consistency | consistent inconsistent | consistently | consistent with |
| corporation | | corporation | corporate | | corporate culture |
| crisis | | crisis | | | economic crisis |
| deny | deny | denial | denied | | deny doing |
| depressing | depress | depression | depressing | depressively | depressing situation |
| deserve | deserve | | | | well-deserved |
| discouraged | discourage | | discouraged | | discourage from |
| diversity | | diversity | diverse | | cultural diversity |
| donate | donate | donation | | | make a donation |
| emphasize | emphasize | emphasis | | | place emphasis on |
| enthusiastic | | enthusiasm | enthusiastic | enthusiastically | enthusiastic about |
| equally | | equality inequality | equal unequal | equally | equally important |
| explicitly | | | explicit | explicitly | explicitly forbidden |
| incredible | | | incredible | incredibly | incredible rate |
| inspire | inspire | inspiration | inspiring | | inspire sb with |
| issue | | issue | | | issue with |
| motivation | motivate | motivation motive | motivational | | lack motivation |
| optimistic | | optimism | optimistic | optimistically | optimistic about |
| passionate | | | passionate | passionately | passionate about |
| perceive | perceive | perception | | | perceived as |
| persuade | persuade | persuasion | persuasive | | persuade sb to do |
| pessimistic | | pessimism | pessimistic | pessimistically | pessimistic view |
| protection | protect | protection | protective | protectively | under protection |
| raise | raise | raise | | | raise awareness, raise funds |
| resource | | resource | resourceful | | limited resources |
| survive | survive | survival survivor | survival | | survival strategy |

| UNIT 7: EXTRA WORDS  <td colspan=7/> |
| allocate | allocate | allocation | | | allocate funds to |
| arise | arise | | | | arise from |
| constrain | constrain | constraint | | | impose constraints on |
| discrimination | discriminate | discrimination | | | discriminate against |
| exploit | exploit | exploitation | | | exploit resources |
| impose | impose | | imposing | | impose on someone |
| obligation | | obligation | obligatory | | obligation to do |
| sufficient | | | sufficient insufficient | sufficiently | sufficient for |

| UNIT 8: READING & WRITING  <td colspan=7/> |
| addiction | addict | addiction | addictive | | addicted to |
| authority | | authority | authoritative | | complete authority |
| care | care | care | careful caring | | take care of |
| complicated | complicate | complication | complicated | | highly complicated |
| concentrate | concentrate | concentration | concentrated | | concentrate on |
| constant | | | constant | constantly | remain constant |
| cure | cure | cure | curable incurable | | cure for an illness |
| diagnose | diagnose | diagnosis | | | diagnose an illness |
| distraction | distract | distraction | distracting | | create a distraction |
| impressive | impress | impression | impressive | impressively | make an impression |
| indicate | indicate | indication indicator | | | indication of |
| intend | intend | intention | intentional | intentionally | intend to do sth |
| involve | involve | involvement | involved | | involved in |
| measure | measure | measurement | | | take measures to |
| monitor | monitor | monitor | | | monitor a situation |
| nutrition | | nutrition nutrient | nutritious | | nutritious diet |
| regard | regard | regard | | | regard as, regardless of |
| procedure | proceed | procedure | | | standard procedure |
| progress | progress | progress | progressive | | make progress |
| recovery | recover | recovery | | | recover from |
| revolutionary | revolutionize | revolution | revolutionary | | revolutionary idea |
| surgery | | surgery surgeon | | | undergo surgery |

| UNIT 8: LISTENING & SPEAKING  <td colspan=7/> |
| approval | approve | approval | approved | | approve of |
| basically | | | basic | basically | basic principles |
| condition | | condition | | | living conditions |
| convince | convince | | convincing convinced | | convince sb to do |
| harmless | harm | harm | harmless | harmlessly | harmless to |
| heal | heal | | | | heal quickly |
| highlight | highlight | highlight | highlighted | | highlight the importance |
| infected | infect | infection | infectious infected | | infected with |
| insist | insist | insistence | insistent | | insist on doing |
| manufacture | manufacture | manufacturer manufacturing | | | manufacture goods |
| predictable | predict | prediction | predictable | predictably | predictable outcome |
| reasonable | reason | reason | reasonable | reasonably | reasonable price |
| release | release | release | | | release from |
| reliable | rely on | reliance | reliable | | reliable data |
| relief | relieve | relief | | | sense of relief |
| remedy | | remedy | remedial | | remedy for |
| restore | restore | restoration | | | restore faith |
| sense | sense | sense | sensible | sensibly | make sense, sense of duty |
| symptom | | symptom | symptomatic | | symptoms of disease |
| undergo | undergo | | | | undergo development |
| valid | | validity | valid invalid | | valid claim |
| variable | vary | variation variety | variable various | | vary from A to B |
| virtual | | | virtual | virtually | virtual reality |
| widely | | | | widely | widely known |

| UNIT 8: EXTRA WORDS  <td colspan=7/> |
| assessment | assess | assessment | | | make assessment |
| budget | | budget | | | on a budget |
| comprehensive | comprehend | comprehension | comprehensive | | comprehensive review |
| digest | digest | digestion | digestive | | easily digestible |
| integrate | integrate | integration | integrated | | integrate into |
| merge | merge | | | | merge with |
| negate | negate | negation | | | negate sth |
| sedentary | | | sedentary | | sedentary lifestyle |
| undertake | undertake | | | | undertake research |

| UNIT 9: READING & WRITING  <td colspan=7/> |
| abandon | abandon | abandonment | abandoned | | found abandoned |
| acquire | acquire | acquisition | | | acquire knowledge/skills |
| aim | aim | aim | aimless | | aim to do sth |
| anticipate | anticipate | anticipation | | | anticipate changes |
| competitive | compete | competition | competitive | competitively | highly competitive |
| considerably | | | considerable | considerably | increase considerably |
| conversation | converse | conversation | | | have a conversation with |
| decline | decline | decline | | | decline in importance |
| dominant | dominate | dominance | dominant | | dominant factor |
| dynamic | | | dynamic | dynamically | dynamic personality |
| emerge | | emerge | | | emerge from |
| expand | expand | expansion | | | expand into |
| force | force | force | | | force sb to do |
| gather | gather | gathering | | | gather data |
| significance | | significance | significant | significantly | attach significance to |
| target | target | target | | | reach a target |
| transformation | transform | transformation | | | undergo transformation |

| UNIT 9: LISTENING & SPEAKING  <td colspan=7/> |
| claim | claim | claim | | | claim to be |
| construct | construct | construction | constructive | | constructive advice |
| curiosity | | curiosity | curious | curiously | satisfy curiosity |
| definitely | | | definite | definitely | definitely say |
| dimensional | | dimension | dimensional | | three-dimensional |
| document | document | documentation | documented | | documented evidence |
| era | | era | | | new era |
| expertise | | expertise expert | expert | | expertise in |
| individual | | individual | individual | individually | treated as individuals |
| mission | | mission | | | core mission |
| ongoing | | | ongoing | | ongoing research |
| ordinary | | | ordinary | ordinarily | ordinary people |
| possession | possess | possession | possessive | | illegal possession |
| propose | propose | proposal | | | propose a plan |
| range | range | range | | | wide range of |
| remains | remain | remains | remaining | | remain silent |
| represent | represent | representative | representative | | represent a change |
| sophisticated | | sophistication | sophisticated | | highly sophisticated |
| universal | | | universal | universally | universal standard |

| UNIT 9: EXTRA WORDS  <td colspan=7/> |
| accompany | accompany | | accompanied | | accompany sb |
| assimilate | assimilate | assimilation | | | assimilate into |
| inherit | inherit | inheritance | | | inherit from |
| interfere | interfere | interference | | | interfere with |
| justice | justify | justice | justified | | social justice |
| minority | | minority | minority | | minority group |
| ratio | | ratio | | | ratio of A to B |
| reinforce | reinforce | reinforcement | | | reinforce a belief |
| upgraded | upgrade | upgrade | upgraded | | upgraded version |

| UNIT 10: READING & WRITING  <td colspan=7/> |
| accurate | | accuracy | accurate inaccurate | accurately | achieve accuracy |
| assistance | assist | assistance | | | offer assistance |
| attempt | attempt | attempt | | | attempt to do |
| civilization | | civilization | civilized | | collapse of civilization |
| classic | | | classic classical | | classic example |
| confused | confuse | confusion | confused confusing | | confused about |
| consist of | consist of | | | | consist entirely of |
| cope | cope | | | | cope with |
| interpret | interpret | interpretation | | | interpret as |
| modify | modify | modification | modified | | modify behavior |
| outcome | | outcome | | | final outcome |
| quit | quit | | | | quit doing |
| recall | recall | | | | recall doing |
| supplemental | supplement | supplement | supplemental | | supplemental income |
| survival | survive | survival | survival | | survival strategy |
| terrifying | terrify | | terrifying terrified | | terrifying experience |
| tough | | | tough | | tough decision |
| underestimate | underestimate | underestimation | | | underestimate importance |
| urge | urge | urge | | | urge sb to do |

| UNIT 10: LISTENING & SPEAKING  <td colspan=7/> |
| anxiety | | anxiety | anxious | anxiously | source of anxiety |
| background | | background | | | background in |
| basis | base | basis | based | | on a regular basis |
| boost | boost | | | | boost confidence |
| confirm | confirm | confirmation | confirmed | | confirmation of |
| evident | | evidence | evident | evidently | become evident |
| notice | notice | notice | noticeable | | noticeable change |
| offensive | offend | offense | offensive | | offensive to |
| processed | process | process | processed | | processed food |
| reaction | react | reaction | | | positive reaction |
| recommend | recommend | recommendation | | | on recommendation |
| reduction | reduce | reduction | | | reduction in |
| secure | secure | security | secure | securely | job security |
| stability | stabilize | stability | stable | | remain stable |
| stimulate | stimulate | stimulation | stimulating | | stimulate growth |

| UNIT 10: EXTRA WORDS  <td colspan=7/> |
| coordination | coordinate | coordination | | | coordination of |
| decay | decay | decay | | | process of decay |
| deliberate | | | deliberate | deliberately | deliberate attempt |
| fundamental | | fundamental | fundamental | fundamentally | fundamental change |
| hesitate | hesitate | hesitation | hesitant | | hesitate about |
| primitive | | | primitive | primitively | primitive tools |
| physiological | | physiology | physiological | physiologically | physiological reaction |
| substantial | | | substantial | substantially | substantial increase |
| unjustly | | | unjust | unjustly | unjustly accused |
"""

vocab_dict = {}

def add_entry(headword, verb, noun, adj, adv, collocation, unit=None):
    headword = headword.strip().lower()
    if not headword or headword == "#":
        return
    if headword not in vocab_dict:
        vocab_dict[headword] = {
            "headword": headword,
            "verb": verb.strip() if verb else None,
            "noun": noun.strip() if noun else None,
            "adjective": adj.strip() if adj else None,
            "adverb": adv.strip() if adv else None,
            "collocation": collocation.strip() if collocation else None,
            "units": []
        }
    else:
        # Merge forms if missing
        if not vocab_dict[headword]["verb"] and verb:
            vocab_dict[headword]["verb"] = verb.strip()
        if not vocab_dict[headword]["noun"] and noun:
            vocab_dict[headword]["noun"] = noun.strip()
        if not vocab_dict[headword]["adjective"] and adj:
            vocab_dict[headword]["adjective"] = adj.strip()
        if not vocab_dict[headword]["adverb"] and adv:
            vocab_dict[headword]["adverb"] = adv.strip()
        if not vocab_dict[headword]["collocation"] and collocation:
            vocab_dict[headword]["collocation"] = collocation.strip()
        elif collocation and collocation not in (vocab_dict[headword]["collocation"] or ""):
            vocab_dict[headword]["collocation"] = f"{vocab_dict[headword]['collocation']} | {collocation.strip()}"

    if unit and unit not in vocab_dict[headword]["units"]:
        vocab_dict[headword]["units"].append(unit)

# Parse Core Table
for line in raw_table.strip().splitlines():
    line = line.strip()
    if not line.startswith("|") or "HEADWORD" in line or "INTERMEDIATE" in line:
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) >= 8:
        headword = parts[2]
        verb = parts[3]
        noun = parts[4]
        adj = parts[5]
        adv = parts[6]
        collocation = parts[7]
        add_entry(headword, verb, noun, adj, adv, collocation, "Core Academic Wordlist")

# Parse Unit Tables
current_unit = "General"
for line in unit_data.strip().splitlines():
    line = line.strip()
    if "UNIT" in line:
        current_unit = line.replace("|", "").replace("<td colspan=7/>", "").strip()
        continue
    if not line.startswith("|") or "HEADWORD" in line:
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) >= 7:
        headword = parts[1]
        verb = parts[2]
        noun = parts[3]
        adj = parts[4]
        adv = parts[5]
        collocation = parts[6]
        add_entry(headword, verb, noun, adj, adv, collocation, current_unit)

result_list = sorted(list(vocab_dict.values()), key=lambda x: x["headword"])
print(f"Total compiled words: {len(result_list)}")

with open("academic_wordlist.json", "w", encoding="utf-8") as f:
    json.dump(result_list, f, ensure_ascii=False, indent=2)

print("academic_wordlist.json saved successfully.")
