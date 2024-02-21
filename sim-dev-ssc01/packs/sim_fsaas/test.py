import json
from datetime import datetime
import math
import pytz

quotas = '''{
"quotas" : 
[
{
"container" : false,
"description" : "",
"efficiency_ratio" : null,
"enforced" : true,
"id" : "NQEAAAEAAAAAAAAAAAAAAAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : null,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511628976,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "default-user",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 0,
"fsphysical_ready" : false,
"inodes" : 0,
"inodes_ready" : true,
"physical" : 0,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.04728005149147727,
"enforced" : true,
"id" : "NQEAAAEAAAAAAAAAAAAAEAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "UID:0"
},
"ready" : true,
"reduction_ratio" : 1.04016113281250,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 313,
"applogical_ready" : true,
"fslogical" : 8521,
"fslogical_ready" : true,
"fsphysical" : 180224,
"fsphysical_ready" : true,
"inodes" : 3,
"inodes_ready" : true,
"physical" : 180224,
"physical_data" : 8192,
"physical_data_ready" : true,
"physical_protection" : 16384,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.8472750407965532,
"enforced" : true,
"id" : "NQEAAAEAAAD9CkkCAAAAFAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "SID:S-1-5-21-2091811888-657802664-3374082997-1438"
},
"ready" : true,
"reduction_ratio" : 1.000167296038852,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 76850314,
"applogical_ready" : true,
"fslogical" : 76966280,
"fslogical_ready" : true,
"fsphysical" : 90839782,
"fsphysical_ready" : true,
"inodes" : 32,
"inodes_ready" : true,
"physical" : 90849280,
"physical_data" : 76947456,
"physical_data_ready" : true,
"physical_protection" : 12763136,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 2,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.8732307480984142,
"enforced" : true,
"id" : "NQEAAAEAAABIPrwCAAAAFAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "SID:S-1-5-21-2091811888-657802664-3374082997-1109"
},
"ready" : true,
"reduction_ratio" : 1.000001410683989,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 11779366958,
"applogical_ready" : true,
"fslogical" : 11779408838,
"fslogical_ready" : true,
"fsphysical" : 13489457241,
"fsphysical_ready" : true,
"inodes" : 12,
"inodes_ready" : true,
"physical" : 13489471488,
"physical_data" : 11779383296,
"physical_data_ready" : true,
"physical_protection" : 1683079168,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 3,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.8479651345456027,
"enforced" : true,
"id" : "NQEAAAEAAAD1jYFKAAAAFAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "SID:S-1-5-21-2091811888-657802664-3374082997-1161"
},
"ready" : true,
"reduction_ratio" : 1.005232647703218,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 1988521546,
"applogical_ready" : true,
"fslogical" : 1992709266,
"fslogical_ready" : true,
"fsphysical" : 2349989622,
"fsphysical_ready" : true,
"inodes" : 1293,
"inodes_ready" : true,
"physical" : 2359345152,
"physical_data" : 1976475648,
"physical_data_ready" : true,
"physical_protection" : 322322432,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 1970,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.9427688881588583,
"enforced" : true,
"id" : "NQEAAAEAAAANQo2JAAAAFAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "SID:S-1-5-21-2091811888-657802664-3374082997-1106"
},
"ready" : true,
"reduction_ratio" : 1.082811327617738,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : true,
"advisory_last_exceeded" : 1666327718,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 86519653147,
"applogical_ready" : true,
"fslogical" : 86520085210,
"fslogical_ready" : true,
"fsphysical" : 91772316945,
"fsphysical_ready" : true,
"inodes" : 113,
"inodes_ready" : true,
"physical" : 97795620864,
"physical_data" : 76129910784,
"physical_data_ready" : true,
"physical_protection" : 11067129856,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 1268331,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.8730049982238539,
"enforced" : true,
"id" : "NQEAAAEAAAAoaEnMAAAAFAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "SID:S-1-5-21-2091811888-657802664-3374082997-1624"
},
"ready" : true,
"reduction_ratio" : 1.000833749232624,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 47777464771,
"applogical_ready" : true,
"fslogical" : 47780255301,
"fslogical_ready" : true,
"fsphysical" : 54730792376,
"fsphysical_ready" : true,
"inodes" : 681,
"inodes_ready" : true,
"physical" : 54766542848,
"physical_data" : 47718055936,
"physical_data_ready" : true,
"physical_protection" : 6845480960,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 7528,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.8671612359366643,
"enforced" : true,
"id" : "NQEAAAEAAADQq6HNAAAAFAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "SID:S-1-5-21-2091811888-657802664-3374082997-5006"
},
"ready" : true,
"reduction_ratio" : 1.001079321334680,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 80864764,
"applogical_ready" : true,
"fslogical" : 80921375,
"fslogical_ready" : true,
"fsphysical" : 93317565,
"fsphysical_ready" : true,
"inodes" : 14,
"inodes_ready" : true,
"physical" : 93388800,
"physical_data" : 80789504,
"physical_data_ready" : true,
"physical_protection" : 11845632,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 15,
"shadow_refs_ready" : true
}
},

{
"container" : false,
"description" : "",
"efficiency_ratio" : 0.00183105468750,
"enforced" : true,
"id" : "NQEAAAEAAACMNTD9AAAAFAIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : true,
"notifications" : "custom",
"path" : "/ifs/plat/home",
"persona" : 
{
"id" : "SID:S-1-5-21-2254907880-988026307-859542710-16571"
},
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 1099511627776,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "user",
"usage" : 
{
"applogical" : 845643360,
"applogical_ready" : true,
"fslogical" : 45,
"fslogical_ready" : true,
"fsphysical" : 24576,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 24576,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 1.913557431144915,
"enforced" : true,
"id" : "hAbbAAEAAAAAAAAAAAAAwAYAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/plat/TEMP-PAAS-NONE-VCD01",
"persona" : null,
"ready" : true,
"reduction_ratio" : 2.240292867748044,
"thresholds" : 
{
"advisory" : 8796093022208,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 10995116277760,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 1807116617076,
"applogical_ready" : true,
"fslogical" : 650925731811,
"fslogical_ready" : true,
"fsphysical" : 340165244699,
"fsphysical_ready" : true,
"inodes" : 490,
"inodes_ready" : true,
"physical" : 668209111040,
"physical_data" : 85051539456,
"physical_data_ready" : true,
"physical_protection" : 15904538624,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 69076409,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 1.738324507553107,
"enforced" : true,
"id" : "mQPpAAEAAAAAAAAAAAAAQAQAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/plat/PLAT-PAAS-SLVR-VCD01",
"persona" : null,
"ready" : true,
"reduction_ratio" : 2.053188661000686,
"thresholds" : 
{
"advisory" : 8796093022208,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 10995116277760,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 788231999565,
"applogical_ready" : true,
"fslogical" : 143211754790,
"fslogical_ready" : true,
"fsphysical" : 82384936856,
"fsphysical_ready" : true,
"inodes" : 247,
"inodes_ready" : true,
"physical" : 149255757824,
"physical_data" : 27859828736,
"physical_data_ready" : true,
"physical_protection" : 5707792384,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 14081032,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.001379229560983175,
"enforced" : true,
"id" : "MwANAQEAAAAAAAAAAAAAwAEAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/plat/wast1/ETH-PRDLOG-Archive",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 8796093022208,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 10995116277760,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 1667362215476,
"applogical_ready" : true,
"fslogical" : 2153658,
"fslogical_ready" : true,
"fsphysical" : 1561493504,
"fsphysical_ready" : true,
"inodes" : 56150,
"inodes_ready" : true,
"physical" : 1561493504,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 1.265859016307218,
"enforced" : true,
"id" : "HgA6AQEAAAAAAAAAAAAAQAMAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/plat/PLAT-PAAS-SLVR-ISO01",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.460648960677142,
"thresholds" : 
{
"advisory" : 8796093022208,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 10995116277760,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 785750212650,
"applogical_ready" : true,
"fslogical" : 785752250409,
"fslogical_ready" : true,
"fsphysical" : 620726510841,
"fsphysical_ready" : true,
"inodes" : 624,
"inodes_ready" : true,
"physical" : 846301593600,
"physical_data" : 396636372992,
"physical_data_ready" : true,
"physical_protection" : 58853457920,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 47499491,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.6027176866074310,
"enforced" : true,
"id" : "EX1sAgEAAAAAAAAAAAAAQAUAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/plat/PLAT-PAAS-SLVR-SCRATCH",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000278924452665,
"thresholds" : 
{
"advisory" : 80530636800,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 107374182400,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 60253980,
"applogical_ready" : true,
"fslogical" : 61194920,
"fslogical_ready" : true,
"fsphysical" : 101531648,
"fsphysical_ready" : true,
"inodes" : 210,
"inodes_ready" : true,
"physical" : 101531648,
"physical_data" : 61177856,
"physical_data_ready" : true,
"physical_protection" : 35061760,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.8718491567261688,
"enforced" : true,
"id" : "FfFFBwEAAAAAAAAAAAAAwAcAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/serv/ppst1/bernie-db-datastore",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000000272075512,
"thresholds" : 
{
"advisory" : 2199023255552,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 5497558138880,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 166520490990,
"applogical_ready" : true,
"fslogical" : 166531019005,
"fslogical_ready" : true,
"fsphysical" : 191008980992,
"fsphysical_ready" : true,
"inodes" : 1510,
"inodes_ready" : true,
"physical" : 191008980992,
"physical_data" : 166530973696,
"physical_data_ready" : true,
"physical_protection" : 23853187072,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0005187988281250,
"enforced" : true,
"id" : "fbJoCAEAAAAAAAAAAAAAwAoAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/ecrp/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 10995116277760,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 34,
"fslogical_ready" : true,
"fsphysical" : 65536,
"fsphysical_ready" : true,
"inodes" : 2,
"inodes_ready" : true,
"physical" : 65536,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0,
"enforced" : true,
"id" : "rkk3GAEAAAAAAAAAAAAAwBQAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/aleg/vb3-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 32768,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 32768,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.8645578655677597,
"enforced" : true,
"id" : "Yx4QGQEAAAAAAAAAAAAAwAwAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/egrp/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000013892837851,
"thresholds" : 
{
"advisory" : 10995116277760,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 951689663580,
"applogical_ready" : true,
"fslogical" : 952236751903,
"fslogical_ready" : true,
"fsphysical" : 1101414711296,
"fsphysical_ready" : true,
"inodes" : 130951,
"inodes_ready" : true,
"physical" : 1101414711296,
"physical_data" : 952223522816,
"physical_data_ready" : true,
"physical_protection" : 143705341952,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.03444417317708334,
"enforced" : true,
"id" : "RhsRKAEAAAAAAAAAAAAAQBMAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/plat/ppst1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.03332519531250,
"thresholds" : 
{
"advisory" : 1099511627776,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 5497558138880,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 336,
"applogical_ready" : true,
"fslogical" : 8465,
"fslogical_ready" : true,
"fsphysical" : 245760,
"fsphysical_ready" : true,
"inodes" : 7,
"inodes_ready" : true,
"physical" : 245760,
"physical_data" : 8192,
"physical_data_ready" : true,
"physical_protection" : 16384,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.8419667958157923,
"enforced" : true,
"id" : "FFIVNAEAAAAAAAAAAAAAQBEAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/serv/pest1/repo",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000025691391276,
"thresholds" : 
{
"advisory" : 5497558138880,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 10995116277760,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 3504866496529,
"applogical_ready" : true,
"fslogical" : 3509977592259,
"fslogical_ready" : true,
"fsphysical" : 4168783863808,
"fsphysical_ready" : true,
"inodes" : 1260740,
"inodes_ready" : true,
"physical" : 4168783863808,
"physical_data" : 3509887418368,
"physical_data_ready" : true,
"physical_protection" : 618141745152,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0,
"enforced" : true,
"id" : "QAqNWQEAAAAAAAAAAAAAwBYAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/mull/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 32768,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 32768,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.7596304306677986,
"enforced" : true,
"id" : "RUMQXQEAAAAAAAAAAAAAQCQAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/mull/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000119742997438,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 9953972114317,
"applogical_ready" : true,
"fslogical" : 9287222089127,
"fslogical_ready" : true,
"fsphysical" : 12225974255616,
"fsphysical_ready" : true,
"inodes" : 11580414,
"inodes_ready" : true,
"physical" : 12225974255616,
"physical_data" : 9286110142464,
"physical_data_ready" : true,
"physical_protection" : 2624799490048,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0,
"enforced" : true,
"id" : "RkMQXQEAAAAAAAAAAAAAQCEAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/oohm/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 32768,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 32768,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.6436115309700480,
"enforced" : true,
"id" : "Bo1BXQEAAAAAAAAAAAAAQB0AAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/fbri/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.001006044244549,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 1319214865644,
"applogical_ready" : true,
"fslogical" : 166748401493,
"fslogical_ready" : true,
"fsphysical" : 259082371072,
"fsphysical_ready" : true,
"inodes" : 2352582,
"inodes_ready" : true,
"physical" : 259082371072,
"physical_data" : 166580813824,
"physical_data_ready" : true,
"physical_protection" : 31933120512,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.7748706181578424,
"enforced" : true,
"id" : "CI1BXQEAAAAAAAAAAAAAQCAAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/gadv/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000284058191708,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : true,
"advisory_last_exceeded" : 1622481937,
"hard" : 49478023249920,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 44582459468295,
"applogical_ready" : true,
"fslogical" : 43985071811983,
"fslogical_ready" : true,
"fsphysical" : 56764407865344,
"fsphysical_ready" : true,
"inodes" : 47227369,
"inodes_ready" : true,
"physical" : 56764407865344,
"physical_data" : 43972581040128,
"physical_data_ready" : true,
"physical_protection" : 11495338885120,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0,
"enforced" : true,
"id" : "GB73XQEAAAAAAAAAAAAAQCIAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/wotk/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 32768,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 32768,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.5577017258976298,
"enforced" : true,
"id" : "jUX-XQEAAAAAAAAAAAAAQB8AAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/ihse/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.002672012360367,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 8885725727055,
"applogical_ready" : true,
"fslogical" : 558394844527,
"fslogical_ready" : true,
"fsphysical" : 1001242812416,
"fsphysical_ready" : true,
"inodes" : 14119277,
"inodes_ready" : true,
"physical" : 1001242812416,
"physical_data" : 556906782720,
"physical_data_ready" : true,
"physical_protection" : 84531134464,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0,
"enforced" : true,
"id" : "vwuFXgEAAAAAAAAAAAAAQBwAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/etsv/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 32768,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 32768,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.7025660993540938,
"enforced" : true,
"id" : "wAuFXgEAAAAAAAAAAAAAQB4AAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/hhvc/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000163155194305,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 3772259205194,
"applogical_ready" : true,
"fslogical" : 3799409764284,
"fslogical_ready" : true,
"fsphysical" : 5407903637504,
"fsphysical_ready" : true,
"inodes" : 7271409,
"inodes_ready" : true,
"physical" : 5407903637504,
"physical_data" : 3798789971968,
"physical_data_ready" : true,
"physical_protection" : 1419167956992,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.5740300627650492,
"enforced" : true,
"id" : "wQuFXgEAAAAAAAAAAAAAQCUAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/makd/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.001521002993316,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 7499156260873,
"applogical_ready" : true,
"fslogical" : 353614295960,
"fslogical_ready" : true,
"fsphysical" : 616020516864,
"fsphysical_ready" : true,
"inodes" : 7732277,
"inodes_ready" : true,
"physical" : 616020516864,
"physical_data" : 353077264384,
"physical_data_ready" : true,
"physical_protection" : 66406842368,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.8285581198166071,
"enforced" : true,
"id" : "LDKHXgEAAAAAAAAAAAAAQBsAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/csol/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000063467214428,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : true,
"advisory_last_exceeded" : 1705220749,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 20659048567528,
"applogical_ready" : true,
"fslogical" : 20364369618381,
"fslogical_ready" : true,
"fsphysical" : 24578082250752,
"fsphysical_ready" : true,
"inodes" : 7830633,
"inodes_ready" : true,
"physical" : 24578082250752,
"physical_data" : 20363077230592,
"physical_data_ready" : true,
"physical_protection" : 3982828814336,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0,
"enforced" : true,
"id" : "n5aabAEAAAAAAAAAAAAAwBkAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/ptch/vb3-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 32768,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 32768,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.8078971540127722,
"enforced" : true,
"id" : "vQ7mbQEAAAAAAAAAAAAAQCMAAAAAAAAA",
"include_snapshots" : false,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/bnlw/vb4-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : 1.000196847654641,
"thresholds" : 
{
"advisory" : 30786325577728,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 38482906972160,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 11343021718330,
"applogical_ready" : true,
"fslogical" : 11374283389025,
"fslogical_ready" : true,
"fsphysical" : 14078875426816,
"fsphysical_ready" : true,
"inodes" : 8175537,
"inodes_ready" : true,
"physical" : 14078875426816,
"physical_data" : 11372044828672,
"physical_data_ready" : true,
"physical_protection" : 2467316006912,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.0,
"enforced" : true,
"id" : "aRZTDgIAAAAAAAAAAAAAwCYAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/ccas/vb3-isi1/pest1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 5497558138880,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 10995116277760,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 0,
"fslogical_ready" : true,
"fsphysical" : 32768,
"fsphysical_ready" : true,
"inodes" : 1,
"inodes_ready" : true,
"physical" : 32768,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
},

{
"container" : true,
"description" : "",
"efficiency_ratio" : 0.00053405761718750,
"enforced" : true,
"id" : "4UiqJwIAAAAAAAAAAAAAwCgAAAAAAAAA",
"include_snapshots" : true,
"labels" : "",
"linked" : false,
"notifications" : "default",
"path" : "/ifs/hcal/vb3-isi1/pefz1",
"persona" : null,
"ready" : true,
"reduction_ratio" : null,
"thresholds" : 
{
"advisory" : 16492674416640,
"advisory_exceeded" : false,
"advisory_last_exceeded" : null,
"hard" : 21990232555520,
"hard_exceeded" : false,
"hard_last_exceeded" : null,
"percent_advisory" : null,
"percent_soft" : null,
"soft" : null,
"soft_exceeded" : false,
"soft_grace" : null,
"soft_last_exceeded" : null
},
"thresholds_on" : "fslogicalsize",
"type" : "directory",
"usage" : 
{
"applogical" : 0,
"applogical_ready" : true,
"fslogical" : 35,
"fslogical_ready" : true,
"fsphysical" : 65536,
"fsphysical_ready" : true,
"inodes" : 2,
"inodes_ready" : true,
"physical" : 65536,
"physical_data" : 0,
"physical_data_ready" : true,
"physical_protection" : 0,
"physical_protection_ready" : true,
"physical_ready" : true,
"shadow_refs" : 0,
"shadow_refs_ready" : true
}
}
],
"resume" : null
}
'''

# Parse JSON data using custom decoder
parsed_data = json.loads(quotas)

# Now you can access the parsed data
#print(len(parsed_data['quotas']))

guid = "f8f21e12bc0c6e76eb5b571ea53483419fd1"
clusterName = "vb3-isi1"
current_datetime_utc = datetime.utcnow()
australia_timezone = pytz.timezone('Australia/Sydney')
current_datetime_australia = pytz.utc.localize(current_datetime_utc).astimezone(australia_timezone)

formatted_datetime = current_datetime_australia.strftime('%Y-%m-%d %H:%M:%S')

scanned_data = []


for obj in parsed_data["quotas"]:
    scanned_data_obj={}
    scanned_data_obj["scanTime"] = formatted_datetime
    scanned_data_obj["clusterName"] = clusterName
    scanned_data_obj["clusterUUID"] = guid
    if 'path' in obj:
        scanned_data_obj['path'] = obj['path']
    if 'container' in obj:
        scanned_data_obj["container"] = obj["container"]
    if 'id' in obj:
        scanned_data_obj['id'] = obj['id']
    if 'include_snapshots' in obj:
        scanned_data_obj["snapshotsIncluded"] = obj['include_snapshots']
    if 'hard' in obj["thresholds"]:
        if obj['thresholds']['hard']!=None:
            hardQuotaGB = math.floor(float(float(float(obj['thresholds']["hard"])/1024)/1024)/1024)
            scanned_data_obj['hardQuota'] = hardQuotaGB 
        else:
            scanned_data_obj['hardQuota'] = obj['thresholds']['soft']    
    if 'thresholds' in obj and 'soft' in obj["thresholds"]:
        if obj["thresholds"]["soft"]!=None:
            softQuotaGB = math.floor(float(float(float(obj['thresholds']["soft"])/1024)/1024)/1024)
            scanned_data_obj['softQuota'] = hardQuotaGB
        else:
            scanned_data_obj['softQuota'] = obj['thresholds']['soft']
    if 'thresholds' in obj and 'advisory' in obj['thresholds']:
        if obj["thresholds"]["advisory"]!=None:
            advisoryQuotaGB = math.floor(float(float(float(obj['thresholds']["advisory"])/1024)/1024)/1024)
            scanned_data_obj['advisoryQuota'] = advisoryQuotaGB
        else:
            scanned_data_obj['advisoryQuota'] = obj['thresholds']['advisory']
    if 'usage' in obj and 'fslogical' in obj['usage']:
        if obj["usage"]["fslogical"]!=None:
            usedQuotaGB = math.floor(float(float(float(obj['usage']["fslogical"])/1024)/1024)/1024)
            scanned_data_obj['usedGB'] = usedQuotaGB
        else:
            scanned_data_obj['usedGB'] = obj['usage']['fslogical']
    if 'usage' in obj and 'fsphysical' in obj['usage']:
        if obj["usage"]["fsphysical"]!=None:
            allocatedQuotaGB = math.floor(float(float(float(obj['usage']["fsphysical"])/1024)/1024)/1024)
            scanned_data_obj['allocatedGB'] = allocatedQuotaGB
        else:
            scanned_data_obj['allocatedGB'] = obj['usage']['fsphysical']
    if 'usage' in obj and 'physical' in obj['usage']:
        if obj["usage"]["physical"]!=None:
            physicalQuotaGB = math.floor(float(float(float(obj['usage']["physical"])/1024)/1024)/1024)
            scanned_data_obj['physicalGB'] = physicalQuotaGB
        else:
            scanned_data_obj['physicalGB'] = obj['usage']['physical']
    if 'usage' in obj and 'physical_protection' in obj['usage']:
        if obj["usage"]["physical_protection"]!=None:
            physicalProtectedQuotaGB = math.floor(float(float(float(obj['usage']["physical_protection"])/1024)/1024)/1024)
            scanned_data_obj['physicalProtectedGB'] = physicalProtectedQuotaGB
        else:
            scanned_data_obj['physicalProtectedGB'] = obj['usage']['physical_protection']
    

    scanned_data.append(scanned_data_obj)

#print(scanned_data)

index=0
metered_data=[]
custid_stier_dict = dict()
custid_stier_index_dict = dict()
count=0
for obj in scanned_data:
    path = obj['path']
    pathArr = path.split('/')
    if len(pathArr) == 5:
        ifs = pathArr[1]
        custid = pathArr[2]
        cluster = pathArr[3]
        stier = pathArr[4]
        
        tempStr = custid + "/" + stier   
        if tempStr in custid_stier_dict:
            custid_stier_dict[tempStr] = custid_stier_dict[tempStr]+obj['usedGB']
            metered_data[custid_stier_index_dict[tempStr]]['usedGB'] = custid_stier_dict[tempStr]
        else:
            metered_data_obj={}
            metered_data_obj['meterTime'] = formatted_datetime
            metered_data_obj['custid'] = custid
            metered_data_obj['storageTier'] = stier 
            metered_data_obj['usedGB'] = obj['usedGB']
            metered_data_obj['dataSource'] = 1   

            custid_stier_dict[tempStr] = obj['usedGB']  
            custid_stier_index_dict[tempStr]=index      
            metered_data.append(metered_data_obj)
            index=index+1

print(metered_data)