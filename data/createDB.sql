create table Departements (
    code_departement TEXT,
    nom_departement TEXT,
    code_region INTEGER,
    zone_climatique TEXT,
    constraint pk_departements primary key (code_departement),
    constraint fk_region foreign key (code_region) references Regions(code_region),
    constraint ck_zoneclimatique check (zone_climatique in ('H1', 'H2', 'H3'))
);

create table Regions (
    code_region INTEGER,
    nom_region TEXT,
    constraint pk_regions primary key (code_region)
);


create table Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    constraint pk_mesures primary key (code_departement, date_mesure),
    constraint fk_mesures foreign key (code_departement) references Departements(code_departement)
);

create table Communes (
    code_commune INTEGER,
    nom_commune TEXT,
    statut_commune TEXT,
    altitude_moyenne_commune INTEGER,
    population_commune INTEGER,
    superficie_commune INTEGER,
    code_canton_commune INTEGER,
    code_arrondissement_commune INTEGER,
    code_departement TEXT,
    constraint pk_communes primary key (code_commune, code_departement),
    constraint fk_communes foreign key (code_departement) references Departements(code_departement)
);

create table Travaux (
    id_travaux INTEGER,
    cout_total_ht_travaux FLOAT,
    cout_induit_ht_travaux FLOAT,
    date_travaux DATE,
    type_logement_travaux TEXT,
    annee_construction_logement_travaux TEXT,
    code_region INTEGER,
    constraint pk_travaux primary key (id_travaux),
    constraint fk_travaux foreign key (code_region) References Regions(code_region)
);

create table Isolations (
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    poste_isolation TEXT,
    isolant_isolation TEXT,
    epaisseur_isolation INTEGER,
    surface_isolation FLOAT,
    constraint fk_isolation foreign key (id_travaux) references Travaux(id_travaux),
    constraint ck_poste check (poste_isolation in ('COMBLES PERDUES', 'ITI', 'ITE', 'RAMPANTS', 'SARKING', 'TOITURE TERRASSE', 'PLANCHER BAS')),
    constraint ck_isolant check (isolant_isolation in ('AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES'))
);

create table Chauffages (
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    energie_avt_travaux_chauffage TEXT,
    energie_installee_chauffage TEXT,
    generateur_chauffage TEXT,
    type_chaudiere_chauffage TEXT,
    constraint fk_chauffages foreign key (id_travaux) references Travaux(id_travaux),
    constraint ck_energieavt_chauffage check (energie_avt_travaux_chauffage in ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    constraint ck_energieinst_chauffage check (energie_installee_chauffage in ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    constraint ck_generateur_chauffage check (generateur_chauffage in ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE', 'RADIATEUR')),
    constraint ck_chaudiere_chauffage check (type_chaudiere_chauffage in ('STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERME', 'HPE'))
);

create table Photovoltaiques (
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    puissance_installee_photovoltaique INTEGER,
    type_panneaux_photovoltaique TEXT,
    constraint fk_photovoltaiques foreign key (id_travaux) references Travaux(id_travaux),
    constraint ck_photovoltaiques check (type_panneaux_photovoltaique in ('MONOCRISTALLIN', 'POLYCRISTALLIN'))
);