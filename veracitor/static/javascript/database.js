var Database = {
    sources : [
    {
        id : 1,
        name : "DN",
        source_type : "New paper agency",
        tag : "sweden",
        description : "A swedish news paper",
        rating : 4
    },
    {
        id : 2,
        name : "Global Terrorism Database (GTD)",
        source_type : "Database",
        tag : "terrorism",
        description : "The Global Terrorism Database (GTD) is an open-source database including information on terrorist events around the world from 1970 through 2011 (with annual updates planned for the future).",
        rating : 5
    },
    {
        id : 3,
        name : "Al-watwan",
        source_type : "Online newspaper",
        tag : "comoros",
        description : "A government-owned national newspaper in Comoros, published in Moroni.",
        rating : 1
    }],
    
    publications : [
    {
        id : 1,
        href : "http://www.dn.se/nyheter/varlden/eldharjade-nattklubbens-agare-gripen",
        title : "Eldhärjade nattklubbens ägare gripen",
        summary : "Polisen grep på måndagen en av ägarna till den eldhärjade nattklubben i sydbrasilianska staden Santa Maria. Även två av de musiker som uppträdde vid tillfället har gripits, uppger officiella källor.",
        source : "DN",
        trustworthy : 4
    },
    {
        id : 2,
        href : "http://www.dn.se/kultur-noje/darin-drommer-om-usa",
        title : "Darin drömmer om USA",
        summary : "Ingen rast, ingen ro för Darin vars \"Så mycket bättre\"-låtar fortfarande röjer på listorna. Nu kommer hans nya skiva \"Exit\", och med den drömmarna om USA, England och Japan.",
        source : "DN",
        trustworthy : 2
    }]
};