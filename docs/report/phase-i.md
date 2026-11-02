# CRISPR Study Workspace

Návrh rozhraní a architektury pro Fázi I projektu ITU 2026

Kapitán a jediný člen: Lukáš Dubšík.

Login: TODO DOPLNIT LOGIN. Cvičení: TODO DOPLNIT DEN A ČAS CVIČENÍ.

Moduly: Prepare, Review a společná infrastruktura. Samostatná účast dohodnuta; rozsah odpovídá dvěma členům.

## Téma projektu

Pracovní prostředí pro přípravu CRISPR analýz a revizi výpočetních výsledků. Aplikace umožňuje připravit identifikovaný požadavek, připojit kompatibilní podklady a uchovat výběr kandidátů s odůvodněním. Obsahuje dva moduly s aktivní změnou dat: Prepare pro požadavky a Review pro rozhodnutí v kolekcích. Export je jejich společný výstup.

Cílovým operátorem je výpočetně orientovaný biolog, bioinformatik nebo výzkumný asistent. Experimentální spolupracovník může přebírat výsledný výběr. Jde zatím o pracovní vymezení rolí; jejich skutečný postup musí ověřit rozhovory.

Lokální aplikace již provádí editaci, validaci podporovaných pravidel, ukládání a import/export. Neprovádí výpočet CRISPR skóre, biologické ověření ani běh kompilátoru IRCOMP. Její JSON není kanonickým jazykem IRCOMP.

TODO před odevzdáním: doplnit dva skutečné rozhovory a jejich dopad do návrhu, login a termín cvičení; zkontrolovat autorství a pravidla využití AI. Tento stav není dokončením povinného primárního výzkumu.

Obsah a čísla stran jsou v editovatelném dokumentu.

<!-- page -->

## 1 Výzkum uživatelských potřeb

### 1.1 Provedený sekundární výzkum a hranice zjištění

Sekundární rešerše z 1. listopadu 2026 zahrnuje 16 zdrojů: sedm veřejných diskusí či hlášení problémů, šest dokumentací a tři původní odborné práce. Zaměřuje se na význam skóre, identitu reference, opravu vstupů, obnovu kontextu a předání výsledků. Úplný registr E01 až E16 je v docs/research/s2-desk-research.md.

Diskuse dokládají popsanou zkušenost konkrétního pisatele, nikoli četnost problému. Dokumentace vysvětluje chování nástroje; neprokazuje obtíže uživatele. Návrhové závěry jsou interpretací těchto podkladů. Rešerše není rozhovorem ani testem použitelnosti.

Konkrétní podklady: autor diskuse o CRISPR skóre uvádí rozdílná hodnocení stejných sekvencí v několika nástrojích [4]. V CRISPOR issue 69 vedla oprava identifikátoru h38 na hg38 k vyřešení hlášeného problému [5]. Galaxy Help obsahuje vyřešený případ nesouladu názvů chromozomů [6]. CHOPCHOP dokumentuje různé významy nul a přetrvávající pokročilá nastavení [8]. Tyto případy odůvodňují zkoumání kontextu a interpretace; neprokazují poruchu všech současných verzí nástrojů.

Existuje i opačná evidence: uživatelům vyhovují zavedená integrovaná prostředí a část výpočetních pracovníků preferuje terminál. Samostatné GUI proto musí přinést užitek větší než převod dat do jeho lokálního formátu. Požadavek na více kolekcí a rozhodování po kandidátech je dosud slabě podložený.

### 1.2 Primární výzkum k doplnění

Pro dobrovolně zvolený rozsah odpovídající dvěma členům jsou plánováni dva skuteční účastníci. K datu této verze nejsou evidována dokončená sezení. Záznamy níže proto nejsou výsledky výzkumu.

| Záznam | Doplnit po skutečném sezení |
| --- | --- |
| P01 | TODO role a relevantní zkušenost, datum, délka, prostředí, souhlas, konkrétní nedávný úkol, použité podklady |
| P02 | TODO role a relevantní zkušenost, datum, délka, prostředí, souhlas, konkrétní nedávný úkol, použité podklady |
| Pozorování | TODO oddělit přímo pozorované kroky od vzpomínek a názorů; odkázat na záznam P01/P02 |
| Vyhodnocení | TODO doložit potřeby, rozpory, funkční současná řešení a skutečné změny návrhu |

Připravený scénář má 35 až 45 minut: poslední úkol, průchod soubory, identita a předání. Koncept se ukazuje až na konci. Osnova je v docs/research/s2-interview-plan.md; citace vyžadují přesný povolený záznam.

<!-- page -->

### 1.3 Pracovní lidské a procesní potřeby

Následující potřeby jsou hypotézy odvozené ze sekundárních zdrojů, nikoli potřeby potvrzené rozhovory. Formulace popisují situaci člověka; konkrétní funkce aplikace následují až v kapitole 3.

| ID | Potřeba a důvod | Podklad a jistota |
| --- | --- | --- |
| N1 | Rozumět původu a významu pozorování, aby rozdílné metriky nebyly zaměněny za stejnou veličinu. | E01, E08, E09, E14; střední |
| N2 | Určit přesný cíl, referenci a konvenci souřadnic, aby výsledek patřil ke správnému vstupu. | E02 až E04, E11; silný technický podklad |
| N3 | Odlišit chybějící informaci od nepříznivého výsledku a přijetí souboru od provedení analýzy. | E08 až E10; dokumentované případy |
| N4 | Poznat opravitelný vstup a zachovat již hotovou práci při opravě. | E03, E04, E10; konkrétní hlášení |
| N5 | Při návratu k práci dohledat vstupy a podklady tehdejšího rozhodnutí. | E06, E15; přenos do této domény neověřen |
| N6 | Předat výběr tak, aby příjemce rozuměl kontextu a nevyřešeným otázkám. | E08, E12; formát předání neověřen |
| N7 | Zapojit nástroj do stávající práce bez nadbytečného převodu a opakovaného zadávání. | E05, E07, E13, E16; také protiváha novému GUI |
| N8 | Zachovat důvod ponechání, vyřazení nebo odložení položky. | Slabá přímá evidence; ověřit granularitu rozhodování |

Jistota označuje podporu existence problému nebo technického pravidla, nikoli statistickou četnost. Identifikátory E odkazují na úplný registr v rešerši; klíčové veřejné zdroje jsou uvedeny i v seznamu literatury.

### 1.4 Převod skutečných zjištění do návrhu

TODO po rozhovorech: ke každé ponechané potřebě připojit konkrétní záznam P01 nebo P02; označit potvrzení, rozpor či neověřený předpoklad. Samostatně uvést pozorovaný krok, jeho dopad a návrhovou interpretaci. Potřeba bez podpory nesmí být přejmenována na výsledek rozhovoru.

Nejrizikovější otázky: začíná operátor skutečně intervaly, rozhoduje po kandidátech, potřebuje alternativní kolekce a dokáže levně dodat očekávaná metadata? Pokud současný notebook nebo skript problém řeší, návrh musí zúžit rozsah nebo využít existující předání. Změny se mají promítnout i do porovnání konkurence, scénářů a priorit, ne pouze do textu této kapitoly.

Pozdější test použitelnosti se soustředí na přípravu cíle, opravu diagnostiky, rozlišení nuly od absence, kompatibilitu revize, změnu rozhodnutí a vysvětlení exportu. Automatizované testy z kapitoly 5 tento výzkum nenahrazují.

<!-- page -->

## 2 Analýza konkurenčních řešení

### 2.1 Metoda a mapování na potřeby

Posouzení z 1. listopadu 2026 zahrnuje CRISPOR, CHOPCHOP, Benchling a Galaxy. První dva jsou přímé doménové alternativy, Benchling integrované laboratorní prostředí a Galaxy obecná alternativa pro organizaci analýz. O značí pozorování veřejného rozhraní, D dokumentované chování a I návrhovou interpretaci. Nebyly prováděny výpočty ani měřeny časy úloh. Vazby N1 až N8 zůstávají pracovní do dokončení rozhovorů.

### 2.2 CRISPOR

Veřejný vstupní formulář verze 5.2 a oficiální manuál [7].

| Hodnocení | Zjištění ve vztahu k tomuto projektu | Potřeby |
| --- | --- | --- |
| Pro 1 O | Tři číslované skupiny spojují cíl, genom a PAM. | N2, N7 |
| Pro 2 D | Odkazy propojují anotovanou sekvenci s řádky kandidátů. | N1, N2 |
| Pro 3 D | Výsledky lze stáhnout pro další práci a archivaci. | N5, N6 |
| Proti 1 D/I | Zapamatovaný genom vyžaduje kontrolu zděděného kontextu. | N2, N4 |
| Proti 2 O/I | Hlavní formulář omezuje jednu sekvenci pod 2300 bp; dávková cesta je oddělená. | N7 |
| Proti 3 D/I | Dlouhodobé uchování vyžaduje vědomé stažení výsledku. | N5, N6 |

Ponaučení: zachovat společný kontext a provázaný detail, ale viditelně oddělit uloženou práci od dočasného výsledku. Posouzení neprokazuje nepřítomnost všech forem poznámek ani nepodporu dávkových úloh.

### 2.3 CHOPCHOP

Veřejný formulář s rozbalenými Options a oficiální instrukce [8].

| Hodnocení | Zjištění ve vztahu k tomuto projektu | Potřeby |
| --- | --- | --- |
| Pro 1 O | Cíl, organismus, nástroj a účel jsou pohromadě. | N2, N7 |
| Pro 2 O | Options oddělují pokročilé volby do tematických záložek. | N7 |
| Pro 3 O | Nabízí identifikátory, souřadnice i vloženou sekvenci. | N2, N7 |
| Proti 1 D/I | Pokročilé volby mohou přetrvat změnu režimu. | N2, N4 |
| Proti 2 D/I | Nula má podle metriky a nastavení různé významy. | N1, N3 |
| Proti 3 O/I | Rozbalené volby vyžadují mnoho doménových rozhodnutí. | N4, N7 |

Ponaučení: postupné odhalování voleb nesmí skrýt účinná nastavení. Uchovat původní nulu a uvést její doložený význam. Třetí nevýhoda je odborný odhad zátěže, nikoli změřené selhání uživatele.

<!-- page -->

### 2.4 Benchling

Posouzen je dokumentovaný CRISPR postup aktualizovaný 26. září 2024 [9]. Přihlášená aplikace nebyla ověřována; všechny funkční popisy níže mají úroveň D.

| Hodnocení | Zjištění ve vztahu k tomuto projektu | Potřeby |
| --- | --- | --- |
| Pro 1 D | Import, analýza a uložené výsledky patří do společného prostředí. | N5, N7 |
| Pro 2 D | Split Workspace propojuje výběr v tabulce s kontextem sekvence. | N1, N2 |
| Pro 3 D | Lze exportovat všechny nebo vybrané guides. | N6, N7 |
| Proti 1 D/I | Popsaná cesta předpokládá účet a prostředí Benchling. | N7 |
| Proti 2 D/I | Příprava přechází mezi importem, parametry a analýzou. | N2, N7 |
| Proti 3 D/I | Popsaný přenos do notebooku zahrnuje TSV a ruční vložení do tabulky. | N6, N8 |

Ponaučení: udržet související objekty spolu a před exportem ukázat kontext i rozhodnutí. Nevýhody se týkají popsané cesty; nejsou tvrzením o všech možnostech produktu. Integrovanost je také argument proti zbytečnému dalšímu organizéru.

### 2.5 Galaxy

Veřejné anonymní prostředí Galaxy Europe a oficiální návody pro historie a workflow [10, 11].

| Hodnocení | Zjištění ve vztahu k tomuto projektu | Potřeby |
| --- | --- | --- |
| Pro 1 D | Historie sdružují práci, anotace a značky. | N5, N8 |
| Pro 2 D | Workflow a nástroje mají dohledatelné verze. | N5 |
| Pro 3 D | Historie lze archivovat a sdílet. | N6 |
| Proti 1 O/I | Obecný katalog a navigace přesahují úzký úkol revize. | N7 |
| Proti 2 D/I | Kontext workflow, verze nástrojů a historie jsou na různých místech. | N2, N5 |
| Proti 3 O | Anonymní relace na posouzeném serveru omezuje správu historií. | N5, N7 |

Ponaučení: převzít dohledatelnost, nikoli rozsah obecné platformy. Omezení anonymní relace není vlastností každého nasazení Galaxy.

### 2.6 Syntéza

Společné návrhové důsledky: viditelný kontext, provázané panely, zřetelný stav uložení a export zachovávající původ podkladů. Nejistá zůstává hodnota nového formátu a kolekcí. Rozsah inspekce vymezují popisy produktů a jejich dokumentace [7 až 11]; nejde o test dokončených uživatelských úloh. Žádná z převzatých interakcí nepřenáší do IRCOMP-GUI vědecké schopnosti těchto produktů.

<!-- page -->

## 3 Návrh uživatelského rozhraní

### 3.1 Zdůvodnění informační struktury

Prepare řeší vyjádření a opravu požadavku (N2, N4). Review řeší význam přijatých podkladů a oddělené rozhodnutí (N1, N3, N8). Export zpřístupňuje uložený kontext pro předání (N5, N6). Trvalý pruh s referencí, profilem, revizí a stavem uložení omezuje nutnost dohledávat souvislosti mezi obrazovkami.

Obrázek 1 Navigace a tok dat z pohledu uživatele. Obrázek je vložen v editovatelném dokumentu.

Přechody mezi třemi pohledy jsou možné bez nového načtení stránky. Výběr zobrazené historické revize mění navigaci, nikoli aktivní požadavek. Výpočet mimo aplikaci je v diagramu hranicí, ne dostupnou funkcí Run.

| Data viditelná pro uživatele | Aktivní operace nad modelem |
| --- | --- |
| Studie, cíl, reference, profil a interval | Vytvořit, přejmenovat, duplikovat; přidat, změnit a odebrat cíl; explicitně nahradit kontext |
| Identita a obsah přijatého evidence bundle | Prohlédnout import a připojit jej ke shodné revizi; originál zůstává neměnný |
| Kolekce, kandidát, stav a zdůvodnění | Vytvořit kolekci, změnit členství M:N, přijmout rozhodnutí a odkazy |
| Pracovní a uložený stav, exportovaný výběr | Save, jednokrokové Undo, znovuotevření; vytvoření konkrétního exportu |

Filtrování a volba položky nejsou počítány jako aktivní změny dat. Podstatnými moduly jsou editace požadavku a editace členství/rozhodnutí.

Běžné úpravy zůstávají v panelech. Diagnostika odkazuje na konkrétní pole; barvu vždy doplňuje text. Na užší obrazovce se oblasti skládají pod sebe. Dodatečné kolekce a technické detaily jsou méně výrazné než první použitelné rozhodnutí. Skutečná srozumitelnost těchto voleb musí projít uživatelským ověřením.

<!-- page -->

### 3.2 Návrhy obou modulů

#### 3.2.1 Prepare a oprava požadavku

Uspořádání tvoří seznam cílů vlevo, editor uprostřed a kontroly vpravo. Seznam udržuje přehled při editaci jedné položky. U vstupů je výslovně uvedena konvence 0-based, end-exclusive; reference a profil jsou společným kontextem.

Obrázek 2 Drátěný model editoru cíle ze S4 čitelný výřez. Obrázek je vložen v editovatelném dokumentu.

Celý drátěný model je v docs/design/wireframes/01-prepare.svg. Výřez ukazuje editovaná data a explicitní souřadnice. Návrhový stav ze S4 není snímkem hotové aplikace.

Scénář A: vytvořit studii, přidat dva cíle a změnit interval. Psaní mění textový buffer. Apply přijme konzistentní hodnoty; změna souřadnic vytvoří novou revizi a současně se aktualizují seznam, souhrn a připravenost exportu. Pouhé přejmenování novou vědeckou revizi netvoří.

Scénář B: zadat neplatný konec intervalu. Přijatá data zůstanou zachována, diagnostika zaměří pole a uživatel opraví vlastní rozepsaný vstup. Save může uložit i neaplikovaný neplatný buffer; tento buffer se po otevření ukazuje odděleně a nevstupuje do exportu.

Scénář C: změnit referenci či profil. Změna vyžaduje explicitní úplnou náhradu kontextu a platných intervalů, bez skryté konverze souřadnic. Dřívější podklady zůstávají přiřazeny původní revizi. Kontrola accession a mezí podle katalogu neověřuje obsah externí FASTA ani biologickou vhodnost.

<!-- page -->

#### 3.2.2 Review a rozhodnutí v kolekci

Seznam kandidátů vybírá středový detail neměnných pozorování. Vpravo je samostatná editovatelná vrstva kolekce a rozhodnutí. Uživatel tak nemusí přepisovat původní pozorování, aby zaznamenal vlastní úsudek.

Obrázek 3 Drátěný model rozhodnutí a odůvodnění výřez ze S4. Obrázek je vložen v editovatelném dokumentu.

Zdrojové hodnoty zůstávají oddělené; nevzniká průměr ani univerzální procento spolehlivosti. Nula je hodnota, absence je jiný stav. Celý návrh je v docs/design/wireframes/03-review.svg.

Scénář D: nejprve zkontrolovat import. Náhled ukáže očekávaný a přijatý kontext, zdroj a kategorii. Připojení je atomické a vyžaduje shodu request ID i celé vybrané revize. Neshodný soubor nelze opravit pouhým přejmenováním reference. Chyba nezpůsobí částečné připojení.

Scénář E: přidat kandidáta do kolekce, zvolit undecided, include for further review, exclude nebo needs clarification a doplnit důvod. Po Apply decision se současně změní řádek, detail i počet nevyřešených položek. Stejný kandidát může mít v jiné kolekci jiné rozhodnutí; jde o vztah M:N.

Scénář F: odstranit členství omylem a použít Undo. Změní se jen rozhodovací vrstva; původní evidence se nemaže. Save uchová studii a samostatné rozepsané buffery pro opětovné otevření. Rozhodnutí není souhlasem k experimentu ani oprávněním spustit výpočet.

<!-- page -->

### 3.3 Export a chybové stavy

Export není třetím samostatným modulem. Sdílí uložený požadavek a výběr kolekcí. Náhled pojmenuje uloženou verzi, revizi, zahrnuté zdroje, závislosti a počet nevyřešených položek. Změny po vytvoření náhledu již jeho bajty nemění.

Obrázek 4 Drátěný model náhledu exportu výřez ze S4. Obrázek je vložen v editovatelném dokumentu.

Při neuložených změnách je nutné Save nebo výslovné Export last saved. Export požadavku obsahuje jednu revizi, nikoli celou historii či buffery. Review export zachovává vybraná rozhodnutí a úplné původní bajty potřebných podkladů s hashi. Stav reviewed znamená dokončenou evidenci rozhodnutí, nikoli vědecké schválení. Nevyřešené položky vedou ke stavu draft.

| Stav | Zobrazení a zotavení |
| --- | --- |
| Prázdná studie / žádné podklady | Konkrétní další krok; žádný vymyšlený výsledek analýzy |
| Neplatný vstup | Diagnostika u pole, zachování bufferu a dříve přijatých dat |
| Selhání Save | Trvalá zpráva, zachování práce, opakování; stav Saved až po potvrzení |
| Zastaralý importní náhled | Nová kontrola vůči aktuální verzi, bez částečné změny |
| Ztracená odpověď příkazu | Zablokovat další změny do obnovení stavu; příkaz slepě neopakovat |
| Starší podklady | Zobrazit původní revizi, nepřeznačit je na aktuální |

Klávesnice používá nativní popsané ovládací prvky a viditelné zaměření. Nevyžádané kontroly nepřesouvají fokus. Ověřené automatizované cesty jsou uvedeny v kapitole 5; úplný audit přístupnosti ani reálné testy použitelnosti dosud provedeny nejsou.

<!-- page -->

## 4 Softwarová architektura GUI a kódový základ

### 4.1 Oddělení pohledů aplikační logiky a dat

React a TypeScript vykreslují sdílený prezentační model. Kontrolér převádí uživatelský záměr na asynchronní HTTP příkaz. Python služby a doména vlastní přijatá data i pravidla. FastAPI zajišťuje transport; SQLite a výměnný formát jsou adaptéry implementující aplikační porty.

Obrázek 5 Vrstvy a tok změny stavu v implementované aplikaci. Obrázek je vložen v editovatelném dokumentu.

Doména ani aplikační služby neimportují React, FastAPI nebo konkrétní SQLite adaptér. Lze je volat bez GUI; testy používají stejné služby. Šipky zobrazují volání při obsluze, zatímco porty vlastní aplikační vrstva a adaptéry na ně závisejí.

| Stav | Vlastník a způsob změny |
| --- | --- |
| Přijatá pracovní studie | Python WorkspaceSession; verzované příkazy |
| Trvale uložená studie a buffery | SQLite; výslovný atomický Save |
| Zrcadlo přijatých dat | TypeScript reducer; náhrada úspěšnou odpovědí |
| Rozepsané řetězce a navigace | Sdílený klientský stav; události z ovládacích prvků |
| Počty a připravenost | Odvozené projekce a selectors; samostatně se nezapisují |

DOM není zdrojem aplikačních dat. Událost Apply vede přes kontrolér a API k doméně; úspěšná odpověď aktualizuje sdílené zrcadlo a všechny závislé panely. Generace bufferu chrání novější psaní před opožděným Save.

<!-- page -->

### 4.2 Specifikace dat a rozhraní modulů

#### 4.2.1 Prepare a jeho datový model

| Typ | Podstatná data a invariant |
| --- | --- |
| Study | study_id, request_id, název, aktivní revize, historie, evidence a kolekce |
| RequestRevision | revision_id, reference_id, profile_id, konvence a cíle; neměnný analytický kontext |
| Target | target_id, accession, start, end, strand; identita přetrvává mezi revizemi |
| TargetDraft | Stejné editované položky jako řetězce; neúplný vstup není přijatým intervalem |
| WorkspaceView | workspace_id, version, base_saved_version, dirty, can_undo, study, diagnostics |

UUID identifikuje studii, požadavek, revizi a cíl. Verze pracovní relace je jiný pojem než vědecká revize nebo uložená verze. Diagnostika má code, severity, location jako JSON Pointer a message; zaměření pole nezávisí na překladu zprávy.

| Příkaz či služba | Vstup | Účinek |
| --- | --- | --- |
| rename_study | title | Kosmetický název, beze změny kontextu |
| apply_target | draft: TargetDraft | Přidání/změna, úplná lokální kontrola; nová revize jen při analytické změně |
| remove_target | target_id | Nová aktivní revize; starší data zůstanou |
| rename_target | target_id, label | Změna popisku bez nové revize |
| set_context | reference_id, profile_id, targets | Atomická náhrada pro stejnou množinu target ID |
| validate_request | revision_id, target_draft | Kontroly passed/failed/not_performed; bez přijetí draftu |
| preview_request / accept_request | přesné bajty / preview_id | Kontrola a otevření nové neuložené studie bez přepsání identity |

PrepareView.tsx vyvolává záměry přes app/controller.ts. Ten používá shared/api.ts a nahrazuje přijaté zrcadlo v app/state.ts. PrepareService v application/prepare.py používá doménové modely a pravidla; pole se nevynucují až v komponentě. Přesné uzavřené datové struktury jsou v application/commands.py a api/requests.py. Názvy zdrojů jsou relativní ke kořeni repozitáře, Python moduly k src/ircomp_gui.

<!-- page -->

#### 4.2.2 Review a jeho datový model

| Typ | Podstatná data a invariant |
| --- | --- |
| EvidenceBundle | bundle_id, request ID, celá revize, kategorie, zdroj, kandidáti, závislosti; originální bajty a SHA-256 |
| CandidateKey | bundle_id a candidate_id; shodný název není shodná identita |
| ReviewCollection | collection_id, název, revision_id a členství |
| MembershipDecision | Klíč kandidáta, disposition, rationale, evidence_refs; jedna položka v jedné kolekci |

Pozorování je neměnné, úsudek patří členství. Podpůrné odkazy musejí ukazovat na připojené kandidáty stejné revize. Nepodložené slučování kandidátů z různých zdrojů není podporováno.

| Příkaz | Vstup | Účinek |
| --- | --- | --- |
| attach_evidence | preview_id | Opětovná kontrola kontextu a atomické připojení bajtů |
| create_collection | revision_id, name | Prázdná kolekce v konkrétní revizi |
| rename_collection | collection_id, name | Změna názvu bez změny členství |
| remove_collection | collection_id | Odstranění kolekce a rozhodnutí, zachování evidence |
| add_member | collection_id, candidate | Nové nerozhodnuté členství; opakování je beze změny |
| remove_member | collection_id, candidate | Odstranění členství a jeho rozhodnutí |
| set_decision | collection_id, candidate, disposition, rationale, evidence_refs | Změna úsudku odděleně od původního záznamu |

ReviewView.tsx používá stejný kontrolér a reducer jako Prepare. ReviewService v application/review.py řeší členství a rozhodnutí; application/imports.py koordinuje náhledy. Neplatný či zastaralý náhled nemění studii. Shodné bundle ID a přesně stejné bajty jsou duplicitou; jiné bajty pod stejným ID jsou blokovanou kolizí.

Všechny měnící příkazy používají POST /api/v1/workspaces/{w}/commands s expected_version, draft_buffers a uzavřeným command. Úspěchem je celý nový WorkspaceView. Serverové operace serializuje lokální zámek; návrh počítá s jedním procesem, nikoli s distribuovanou kolaborací.

<!-- page -->

### 4.3 Společné API a trvalé uložení

| Cesta pod /api/v1 | Operace a výsledek |
| --- | --- |
| GET /catalogue; GET /studies | Podporované reference/profily; seznam uložených studií |
| POST /workspaces | source new, saved, duplicate nebo request_import; 201 WorkspaceView |
| GET nebo DELETE /workspaces/{w} | Čtení relace nebo potvrzené zavření; uloženou studii nemaže |
| POST /workspaces/{w}/commands | Verzovaný příkaz; 200 WorkspaceView |
| POST /workspaces/{w}/validate | Lokální kontroly přijaté revize a samostatného draftu |
| POST /workspaces/{w}/save; /undo | Atomický Save s verzemi; jednokrokové Undo |
| POST /imports; DELETE /imports/{id} | Neměnný náhled / jeho zrušení, bez částečné změny studie |
| POST /exports; GET /exports/{id}/file | Zmrazený náhled a přesně jeho bajty |
| GET /examples/{name} | Čtyři předem označené syntetické příklady, nikoli výsledky běhu |

Přesná specifikace dat a chyb je v docs/architecture/api.md a běhovém /openapi.json. HTTP adaptér pouze převádí typy a chyby; pravidla kompatibility, intervalů a dokončenosti patří službám a doméně.

Save zapisuje celý omezený agregát v jedné SQLite transakci. Jediná tabulka studies obsahuje study_id, unikátní request_id, saved_version, title, updated_at a document_json. SQL verze je PRAGMA user_version = 1; vztahy mezi objekty ověřuje doména, nejsou vydávány za samostatné SQL tabulky. Zápis s očekávanou saved_version brání přepsání novější kopie. Chyba vrací původní uložený stav.

Po načtení se kontrolují verze, obálka, identity, odkazy a hashe původních bajtů. Neznámý či poškozený formát se nepřepisuje automatickou opravou. Undo vrací poslední přijatý pracovní snímek včetně bufferů; po Save se historie Undo čistí.

Chyba má error.code, message, diagnostics a případnou workspace_version. Konflikt 409 vyžaduje obnovu či nové potvrzení, ne tichý přepis. Validační chyba 422 vede ke konkrétnímu vstupu; překročení limitu 413 k menším datům. Při selhání persistence 503 zůstává práce k opakování. Ztracená odpověď může skrývat přijatý příkaz, a proto klient nejprve obnoví autoritativní stav.

<!-- page -->

### 4.4 Výměnné formáty a hranice vůči IRCOMP

Lokální formát 1.0 je UTF-8 JSON s JSON Schema 2020-12. request obsahuje jednu identifikovanou revizi, evidence deklarovaný zdroj a kandidáty, review vybrané kolekce a úplné potřebné source soubory jako base64 s SHA-256. Import review balíčku není součástí této verze; export požadavku není úplná záloha pracovní studie.

Kompatibilita evidence vyžaduje request ID a celou revizi: UUID, referenci, profil, konvenci i cíle s identitami a intervaly. Pořadí cílů se ignoruje; popisky nejsou vědeckým kontextem. Starší podklady lze otevřít jen vůči výslovně vybrané uchované revizi.

| Omezení lokální aplikace | Hodnota a význam |
| --- | --- |
| Import / hloubka JSON | 1 MiB dekódovaných bajtů / 32 úrovní |
| Cíle / revize | 50 / 200 na studii |
| Evidence / kandidáti / metriky | 10 bundles; 200 kandidátů na bundle; 20 metrik na kandidáta |
| Kolekce / členství | 20 kolekcí; 1000 členství ve studii |
| Uložený snímek / review export | Nejvýše 20 MiB výsledné serializace |

Jde o zvolené meze malého lokálního projektu, nikoli výsledky výkonnostního měření. Parser odmítá duplicitní klíče, ne konečná čísla, neznámé verze a neplatné odkazy. Přijatý JSON samotný neprokazuje správný kontext.

Katalog obsahuje syntetický demo_contig a explicitní podmnožinu GRCh38.p14: 24 jaderných chromozomů, accession a délky z NCBI assembly reportu [12]. Neobsahuje mitochondrii, alternativní ani patch sekvence. Neověřuje FASTA. Profily deklarují SpCas9/NGG a preexperimentální záměr, neprovádějí výpočet.

IRCOMP vlastní formální jazyk, normalizovaný request, cartridge, cíle, omezení, plánovač, kompilátor a řízení spuštění [13]. GUI vlastní pracovní editaci a revizi. Budoucí verzovaný adaptér smí předat pouze úplný podporovaný význam; chybějící cartridge verzi, cíle, obecná omezení a AI pravidla nesmí domyslet. YAML editor, workflow graf, compile/execute a vědecké běhy jsou odloženy v docs/architecture/ircomp-integration.md. Současné validace nemají autoritu kompilátoru.

<!-- page -->

## 5 Zdrojové kódy a funkční základ

### 5.1 Implementované rozhraní a ověření

Stav implementace odpovídá commitu 9364e16 z 2. listopadu 2026. Přesné příkazy, záběr a omezení kontrol jsou v docs/verification.md. Nejde o výsledky uživatelských sezení.

Obrázek 6 Implementovaný Review výřez původních metrik ze syntetického příkladu S6. Obrázek je vložen v editovatelném dokumentu.

Snímek skutečné aplikace ukazuje numerickou nulu a samostatné not supplied. Editor rozhodnutí mění rozhodovací vrstvu, nikoli původní hodnoty. Výřez je přímo součástí této zprávy.

| Kontrola provedená v S6 | Zjištěný výsledek a hranice |
| --- | --- |
| Backend | 33 úspěšných pytest případů: služby, persistence, import/export, HTTP a směr závislostí |
| Klient | Striktní TypeScript a produkční Vite build; sedm Chromium workflow |
| Statické kontroly | Pyright bez chyb a varování, Ruff a formátování; Prettier |
| Kontrakty | Schema, devět strukturálních očekávání fixtures, původní bajty a provenance katalogu |
| Instalace | Čistý Git archiv a npm ci/build; sdist a samostatně instalovaný wheel s balenými zdroji |

Prohlížečové scénáře zahrnují Save a otevření, rozhodnutí, neplatné buffery, opožděný Save, diagnostiku s fokusem, dvě kolekce, starou revizi, ztracenou odpověď a export posledního uloženého stavu. Úzké rozložení bylo kontrolováno na šířce 390 px. Tyto případy neprokazují obecnou použitelnost, všechny prohlížeče ani úplnou přístupnost.

<!-- page -->

### 5.2 Rozdělení zdrojových souborů

Oba moduly spadají do dohodnuté samostatné práce Lukáše Dubšíka. Níže jsou odpovědnosti zdrojů, nikoli tvrzení, že externí knihovny byly vytvořeny v projektu. TODO před odevzdáním: ověřit vlastní porozumění, skutečný autorský podíl a požadované hlavičky; současné hlavičky ještě uvádějí review pending.

Python soubory níže jsou relativní ke src/ircomp_gui. Sdílený základ označuje infrastrukturu společnou oběma modulům, nikoli dalšího člena týmu.

| Část | Zdrojové soubory a odpovědnosti |
| --- | --- |
| Prepare GUI | web/src/features/prepare/PrepareView.tsx |
| Prepare logika | application/prepare.py; domain/catalogue.py, rules.py; sdílené modely |
| Review GUI | web/src/features/review/ReviewView.tsx |
| Review logika | application/review.py, imports.py; sdílené modely a validace |
| Export | web/src/features/export/ExportView.tsx; application/export.py |
| Klientský model a řízení | web/src/app/App.tsx, WorkspaceProvider.tsx, controller.ts, state.ts, selectors.ts |
| Klientská hranice | web/src/shared/api.ts, types.ts, ImportPreview.tsx; web/src/main.tsx, styles.css; web/index.html |
| Doména | domain/models.py, rules.py, errors.py, catalogue.py, serialization.py |
| Aplikační základ | application/workspace.py, commands.py, ports.py |
| Adaptéry a HTTP | adapters/sqlite.py, exchange.py, resources.py; api/app.py, requests.py; __main__.py |
| Automatizované kontroly | tests/test_workspace.py; web/e2e/workspace.spec.ts; scripts/development/check_contracts.py |
| Kontrakty a konfigurace | contracts/exchange.schema.json, catalogue.json, cases.json, examples; pyproject.toml, requirements-dev.lock; web/package.json, package-lock.json, vite.config.ts, playwright.config.ts; balíčkové __init__.py |

Přesná veřejná API a návratové typy jsou popsány v kapitole 4 a v běhovém OpenAPI. Revizi zdrojového archivu a kontrolní součet eviduje S8 v adresáři submission; postup a další kontroly jsou v docs/submission.md. Závislosti zůstávají externími projekty se svými licencemi.

<!-- page -->

### 5.3 Spuštění a stav odevzdání

Ověřené prostředí je Linux, Python 3.14.6, Node 20.20.2 a npm 10.8.2. Deklarováno je Python nejméně 3.12 a Node nejméně 20.19; jiné verze nebyly tímto záznamem ověřeny. Z kořene zdrojů:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.lock
.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
npm --prefix web ci
npm --prefix web run build
.venv/bin/ircomp-gui
```

Prohlížeč otevře http://127.0.0.1:8000; interaktivní API je /docs. Server běží v jediném procesu. Uložené studie jsou standardně v ~/.local/share/ircomp-gui/workspace.sqlite3. Proměnná IRCOMP_GUI_DATABASE volí jinou databázi; instalační postup vyžaduje dostupné deklarované balíčky.

Save je výslovný. Restart serveru ztratí neuložené relace a náhledy. Obnovení stránky se může připojit k existující relaci, ale samotné dosud neodeslané psaní nemá zaručenou obnovu. Načtení posledního uloženého stavu není totéž co obnova veškeré neuložené práce.

| Výstup nebo kontrola | Stav této verze |
| --- | --- |
| Lokální model/API a klíčové GUI | Implementováno a ověřeno v rozsahu S6 |
| Čtyři konkurenti, wireframes, architektura | Připraveno; vazby na skutečný výzkum čekají na rozhovory |
| Dva skutečné rozhovory | TODO provést, zapsat a promítnout do návrhu |
| Login a termín cvičení | TODO doplnit na identifikační straně |
| Autorské označení a pravidla AI | TODO věcná kontrola; samotný název v nadpisu ji nenahrazuje |
| 00_DOPLNIT_LOGIN_source.zip | S8: zdrojový archiv a kontrolní součet v adresáři submission; ověřit aktuální revizi |
| Finální kontrola a Moodle | S9 až S10: TODO; termín 6. 11. 2026 ve 23:59 |

Kontrolní prezentace proběhne v termínu cvičení v týdnu od 9. listopadu 2026. Předvede oba moduly, změny sdíleného stavu, opravu chyby, Save/otevření a odpovídající API. Konkrétní slot je k doplnění. Podle dodaného Moodle záznamu jsou všechny části a demonstrace povinné; neúplnost může vést k 0 bodům a pozdní odevzdání k penalizaci 5 bodů. Tato zpráva nenahrazuje záznam skutečného odevzdání.

<!-- page -->

## 6 Zdroje a podklady

### 6.1 Zadání a původ projektových podkladů

[1] ITU. Zadání a pokyny k projektu 2026. Dodaný soubor DOCX; zejména výzkum, rozhraní a model, autorství a pravidla AI. Moodle výpis dodaný z přístupu studenta uvádí termín Fáze I 6. listopadu 2026 ve 23:59 a prezentace od 9. listopadu.

[2] ITU. Fáze I Design report šablona. Dodaný DOCX; struktura této zprávy, identifikace, výzkum, konkurence, UI, architektura a související kódy.

[3] ITU. Průvodce uživatelským výzkumem a testováním použitelnosti. Dodaný DOCX; příprava a záznam reálných sezení. Veřejné diskuse nejsou náhradními respondenty.

Lokální projektové podklady: docs/research/s2-desk-research.md a s2-interview-plan.md; docs/design/README.md a SVG návrhy; docs/architecture/overview.md, domain-model.md, api.md, exchange-and-persistence.md a ircomp-integration.md. Pozorované technické výsledky: docs/verification.md, implementace 9364e16. Tyto materiály rozlišují zamýšlené chování, implementaci a ověřené případy.

### 6.2 Veřejné podklady výzkumu a srovnání

Níže jsou klíčové zdroje z rešerše a posouzení provedených 1. listopadu 2026. Datum se vztahuje k zaznamenané inspekci, nikoli k tvrzení o novém měření. Úplný registr dalších zdrojů a jejich limitů zůstává v uvedených pracovních podkladech.

[4] r/labrats. Why are on/off target scores so variable. Zkušenost autora diskuse; přesné datum příspěvku nebylo ověřeno. https://www.reddit.com/r/labrats/comments/tlaqhf/why_are_onoff_target_scores_so_variable_from/

[5] CRISPOR GitHub issue 69. Záznam od 7. srpna 2024; v závěru oprava identifikátoru reference. https://github.com/maximilianh/crisporWebsite/issues/69

[6] Galaxy Help. Help with VCF annotation. Diskuse 4. až 10. ledna 2024; odlišné pojmenování chromozomů. https://help.galaxyproject.org/t/help-with-vcf-annotation/11407

[7] CRISPOR. Veřejný formulář a oficiální manuál. https://crispor.gi.ucsc.edu/ a https://github.com/maximilianh/crisporWebsite/blob/master/manual/manual.md

<!-- page -->

### 6.3 Dokumentace nástrojů a technické hranice

[8] CHOPCHOP. Veřejný formulář, Options a Instructions. https://chopchop.cbu.uib.no/ a https://chopchop.cbu.uib.no/instructions

[9] Benchling. CRISPR Knockouts. Oficiální postup aktualizovaný 26. září 2024; dokumentační, nikoli přihlášená inspekce. https://help.benchling.com/hc/en-us/articles/9684226093197-CRISPR-Knockouts

[10] Galaxy Europe a Galaxy Training Network. Historie a jejich správa. https://usegalaxy.eu/ a https://training.galaxyproject.org/training-material/topics/galaxy-interface/tutorials/history/tutorial.html

[11] Galaxy Training Network. Workflow editor a verze nástrojů. https://training.galaxyproject.org/training-material/topics/galaxy-interface/tutorials/workflow-editor/tutorial.html

[12] NCBI. GRCh38.p14 assembly report, GCF_000001405.40. Podklad accession a délek 24 jaderných chromozomů; stažený originál a jeho SHA-256 jsou v contracts/references a katalogu. https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_assembly_report.txt

[13] IRCOMP. Návrh input/output/error contract, inspekce revize ffde336832dfa8250e4051b9c7f785009ff1e4e8. Navrhovaný, nikoli zmrazený běhový kontrakt. https://github.com/viridisquercus/IRCOMP/blob/ffde336832dfa8250e4051b9c7f785009ff1e4e8/docs/architecture/contracts/input-output-error-contract.md

Obrázky 1 a 5 jsou projektová schémata. Obrázky 2 až 4 jsou výřezy návrhů S4, obrázek 6 je výřez implementace S6. Veškerá zobrazená kandidátní data jsou syntetická. Obrázky nejsou výsledkem provedeného genomického výpočtu ani uživatelského testu.
