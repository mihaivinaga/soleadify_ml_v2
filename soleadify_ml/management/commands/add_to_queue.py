from tqdm import tqdm
from django.core.management.base import BaseCommand
from soleadify_ml.models.category_website import CategoryWebsite
from soleadify_ml.tasks import scrapping


class Command(BaseCommand):
    help = "Add to queue"

    def handle(self, *args, **options):
        website_ids = [4084722,4610571,4809330,4903488,7676853,7683831,7683917,7692037,7702867,7704040,7703393,7704327,7721831,7742417,7742873,7743097,7743735,7744356,7745264,7745427,7745431,7745693,7745837,7745886,7745985,7746328,7746245,7746285,7746598,7746607,7747005,7747189,7746595,7747138,7746992,7747579,7747812,7747871,7748238,7748478,7748069,7749501,7750356,7750645,7751578,4152751,3013533,3014364,3011717,3025891,3022999,3019785,3013404,3019965,3029914,3019495,3035499,3043121,3043610,3045149,3028451,3043747,3045479,3048361,3046648,3048467,3036657,3051673,3053831,3054997,3049992,3062990,3067565,3055074,3070194,3059641,3074449,3051177,3070707,3087654,3088579,3078022,3064204,3081254,3090551,3087430,3075838,3103429,3105087,3103118,3106248,3098623,3108641,3090334,3092472,3123383,3126197,3097594,3116494,3130995,3131823,3107463,3132265,3119185,3133299,3131011,3139253,3139734,3139967,3137358,3140661,3129259,3124002,3149682,3135924,3148294,3149364,3156357,3167798,3166588,3168566,3171520,3155407,3159770,3162846,3170995,3170456,4173813,3169131,3184168,4182029,4213510,4213456,4205213,4236979,4214058,4231222,4218454,4238920,4222928,4245519,4278739,3209907,3220341,3215283,3215756,3215991,3212978,3255937,3231457,3265933,3239291,3229150,3214115,3241836,3214486,3252242,3251253,3252184,3252450,3234985,3280734,3246518,3247667,3298413,3378828,3386635,4298713,4310524,3404436,3387741,4337212,3402255,3399536,3399744,3401753,3412389,3458145,3413085,3451832,3426036,3471793,3465549,3451215,3500819,3467014,3487824,3436252,3462733,3516124,3446126,3476686,3489218,3491099,3463955,3448995,3529469,3534813,3540413,3527783,3506597,3516021,3486161,3549512,3528423,3506670,3540876,3557385,3547672,3542983,3608012,3558093,3611167,3541432,3587515,3600195,3606606,3618430,3628549,3567848,3619879,3640478,3648030,3645372,3648101,3596674,3652600,3679289,3662442,3685045,3666537,3617787,3681038,3698749,3679407,3662108,3673273,3706642,3724598,3661874,3667622,3716510,3646025,3720271,3717591,3732267,3739843,4356566,4361486,4399916,4349973,4374829,3811319,3803727,3804638,3823274,3836904,3830976,3837233,3821709,3843784,3872876,3845364,3843641,3905179,3867681,3876954,3913074,3910401,3918737,4026425,4084456,4067705,4093790,4099146,4108234,4416047,4120423,4437623,4133084,4449508,4416318,4548324,6150631,4547578,4550840,6228621,6152969,6097433,6232019,6251845,6282260,6349710,6260628,6365087,6446390,6477248,6483060,6519794,4658789,4650444,4697538,4688120,4693836,4662731,4673064,4814116,4792141,4789982,4781491,4835516,4788710,4851511,4806185,4848731,4804132,4862549,4805665,4821450,4881412,4780668,4877696,4833653,4851298,4835152,4793719,4861782,4822687,4796872,4809022,4823238,4845064,4869985,4803291,4869853,4875541,4882758,4891722,4878169,4912590,4908055,4857161,4846144,4876779,4875756,4852827,4852492,4898595,4889191,4901811,4871562,4903750,4957259,4904222,4921346,4918885,4949438,4919716,4929952,4924362,4895762,4934659,4941586,4929685,4925832,4917330,4910573,4940391,4955246,4933306,4909998,4950681,4936709,4953971,4972097,4939868,5002950,4932070,5013302,4967785,5024348,4978785,4991624,4952299,4992248,4965215,4979953,4989233,4971114,5023598,4991024,5013583,4981220,4977580,5020643,5023619,5031390,5041680,4994824,5023503,5060091,5039690,5050323,5058589,5062193,5073195,5046380,5015862,5099964,5086662,5075811,5112804,5124178,5069902,5126148,5127414,5095321,5102260,5072302,5054890,5145680,5113437,5154725,5099439,5065309,5072382,5105751,5065189,5162350,5121453,5112946,5131472,5122416,5125680,5197246,5133552,5169135,5130608,5213395,5118895,5165762,5157812,5218723,5216275,5163382,5178239,5156887,5129685,5164830,5182868,5185040,5188048,5134989,5171792,5178530,5168165,5141705,5190964,5207333,5191074,5177244,5199939,5180263,5183712,5182300,5198994,5258400,5264425,5255596,5310683,5308127,5336300,5304224,5333266,5395548,5469667,5417435,5419182,5393472,5489297,5437950,5515373,5462716,5468631,5566787,5475059,5693638,5489290,5669558,5588816,5751821,5613846,5847922,5851251,5712558,5908836,5901121,6695721,5961406,6561351,5892178,6751145,6742554,6696772,6611133,6861517,6632270,6707186,6801698,6905762,6821703,6854343,7058275,6874669,6937262,7034464,7067788,7089797,7037464,7239682,7098621,7370879,7312892,5951832,5971755,5985070,7354540,5965888,5959129,5976310,6014219,6000756,6008261,6012900,6015984,6010116,5959175,6004648,6019862,5974139,5981791,5972871,6013127,6047631,7377390,6016428,6007124,6035451,6015508,5989904,6031185,7461611,6049812,7490734,5992399,6029278,7532402,7461412,7454578,7518624,7654198,7665768,7718892,7669779,7669771,7669804,7669738,7669806,7713055,7669705,7669825,7675431,7669725,7675443,7675406,7721583,7675503,7675739,7675520,7714299,7675787,7675875,7676016,7675894,7675890,7675726,7675831,7676208,7676284,7675936,7676178,7676168,7676457,7676028,7676217,7676023,7669763,7676387,7676872,7669780,7676503,7676757,7676699,7676096,7676390,7675547,7676766,7677066,7677239,7675637,7675590,7676741,7676733,7676866,7669753,7677004,7676015,7675512,7675580,7675626,7669803,7721779,7675935,7676225,7676098,7676386,7677876,7676145,7675716,7676126,7677622,7676865,7677679,7676313,7676834,7677061,7675392,7676405,7677835,7676244,7676357,7676732,7676433,7676711,7677586,7676998,7676735,7678562,7676965,7679273,7678508,7679300,7680518,7678009,7678537,7679660,7680498,7680936,7680960,7680271,7679864,7679126,7680760,7681319,7681856,7682103,7679922,7682334,7680154,7682885,7681868,7680931,7681084,7682756,7681741,7683440,7684068,7681586,7683375,7681573,7683530,7684817,7685047,7683920,7683007,7685543,7686353,7684079,7684104,7684748,7685740,7684972,7684625,7683669,7684659,7685009,7688472,7686059,7686132,7688977,7687534,7688427,7688870,7685963,7688537,7689526,7688981,7689385,7688222,7691051,7688257,7688721,7690003,7690035,7691847,7689389,7689060,7691276,7689843,7689733,7690432,7690565,7692878,7689960,7691473,7693501,7690653,7690962,7693030,7692285,7692756,7694925,7692329,7699770,7692227,7692924,7692482,7696350,7697025,7698465,7697538,7697402,7699141,7700354,7701925,7700590,7701284,7700777,7700877,7702291,7703363,7702624,7702707,7703259,7702696,7703030,7703255,7701029,7704242,7703079,7703317,7703460,7702536,7701797,7703897,7704107,7704570,7703345,7703361,7703583,7701703,7704648,7704318,7704322,7703485,7704175,7703329,7702497,7703245,7703458,7742351,7703680,7703538,7704208,7721609,7742334,7704321,7703616,7703547,7742320,7742333,7742318,7742285,7703631,7742361,7742331,7742355,7742322,7742433,7742396,7742372,7702993,7742459,7742349,7742690,7742508,7702578,7703993,7743113,7742501,7742496,7742594,7743034,7703154,7704157,7742342,7703850,7743337,7743256,7704138,7703236,7742400,7704194,7704062,7704656,7743186,7742848,7743153,7742313,7703814,7743402,7743257,7704301,7743192,7742780,7743073,7742450,7742306,7742367,7704010,7742385,7703950,7742369,7743336,7743399,7742960,7743191,7743218,7743040,7743427,7743230,7743422,7743334,7743264,7743198,7743455,7742488,7743248,7704414,7743350,7743530,7743590,7703331,7704313,7703702,7743657,7743296,7743484,7743465,7743651,7743654,7743510,7743390,7743586,7743067,7703525,7743648,7743080,7743759,7703518,7743926,7743884,7703605,7703550,7703734,7743784,7743724,7743118,7722079,7743127,7744162,7742319,7744760,7743147,7743210,7744247,7744277,7742604,7744079,7742357,7703746,7743327,7744536,7743983,7743420,7743320,7743619,7744231,7744737,7744256,7744243,7703146,7744259,7743461,7744704,7744473,7742401,7742383,7742422,7744392,7744701,7742364,7744768,7742489,7704053,7743144,7743792,7742330,7742522,7743896,7744842,7742391,7744369,7745104,7743201,7743780,7744979,7744796,7742324,7744973,7743706,7742283,7743881,7704731,7742443,7744338,7742831,7744066,7743871,7742458,7742532,7745414,7743462,7745250,7744281,7742810,7744347,7744427,7745389,7742712,7745376,7742784,7743442,7745041,7742700,7744327,7743322,7745594,7745606,7745413,7743265,7745706,7745474,7745394,7743503,7745400,7744771,7745749,7745523,7744851,7745609,7745565,7743331,7745448,7744770,7745678,7743045,7744661,7745952,7744708,7745960,7744030,7745705,7745511,7745908,7743741,7743433,7743207,7743189,7744016,7744155,7745961,7745725,7745866,7746106,7743565,7745854,7743419,7743245,7744847,7742352,7742464,7745781,7744469,7743847,7746060,7746378,7745049,7742325,7744130,7742317,7745166,7745215,7744479,7742397,7746095,7746277,7743843,7746204,7746367,7743864,7742491,7742684,7743696,7744291,7745096,7746411,7743887,7744675,7746345,7742739,7744630,7746278,7744562,7746805,7746260,7746416,7746511,7746300,7744641,7744742,7744007,7742934,7743951,7742936,7745629,7744270,7745616,7746735,7743169,7744271,7746445,7745664,7745944,7744149,7743171,7744065,7743405,7745628,7745005,7743260,7746786,7745655,7743290,7744246,7745883,7745764,7745879,7744262,7743518,7743486,7743559,7743254,7746838,7746899,7746033,7743409,7743285,7743443,7744766,7747111,7744669,7746079,7745977,7745588,7747118,7744826,7745330,7745791,7747457,7747513,7743637,7745755,7745939,7745873,7746964,7743839,7747277,7745929,7747211,7747222,7747186,7747403,7747455,7746000,7745747,7746225,7746251,7747839,7747593,7745951,7746131,7747727,7747278,7747535,7747716,7747539,7747806,7744558,7746399,7747808,7747473,7744209,7747616,7745849,7747580,7747551,7748066,7745538,7747558,7745955,7747480,7746223,7747425,7744591,7747630,7745416,7747766,7747598,7747563,7747788,7745418,7747651,7745449,7747840,7745712,7747614,7745710,7746653,7746414,7744416,7745627,7744613,7746571,7747977,7745855,7746835,7745934,7746882,7745968,7745809,7745833,7745651,7745865,7746064,7746935,7745235,7745842,7745999,7745814,7748580,7746885,7746058,7746927,7745313,7745350,7745850,7746949,7745899,7748410,7748222,7745770,7746046,7746184,7746088,7747322,7745323,7747049,7745301,7749316,7747881,7745517,7745631,7745707,7747019,7746295,7747411,7747027,7745613,7749023,7747701,7748801,7747137,7749457,7747503,7747743,7747463,7746545,7745919,7745554,7748994,7747482,7748099,7747490,7749045,7747885,7746784,7749407,7747547,7747836,7747354,7747622,7747612,7745996,7746999,7746066,7747509,7745941,7747689,7748193,7748053,7747757,7746078,7749165,7747254,7748055,7746208,7749295,7749534,7749482,7748104,7746138,7746633,7748286,7749544,7746394,7748167,7746369,7746340,7749645,7747224,7748142,7748434,7747134,7750512,7749671,7747431,7748561,7747351,7749753,7748397,7747486,7747523,7748850,7747573,7747569,7747417,7747813,7747643,7746813,7747002,7748471,7747686,7748641,7747109,7748583,7748835,7748087,7750710,7747038,7748832,7750625,7748967,7747141,7750388,7750472,7750192,7748780,7750501,7746910,7748991,7749314,7748185,7747343,7751137,7748330,7747271,7747117,7747497,7749644,7750947,7751828,7749348,7747647,7749462,7749762,7747428,7747730,7747423,7747851,7747878,7751661,7751651,7747618,7749732,7747798,7751854,7747635,7747621,7751533,7751635,7750260,7751151,7752031,7750239,7751268,7750272,7749357,7751187,7749903,7750332,7749720,7751972,7752048,7751544,7751501,7751785,7749539,7751551,7749496,7752135,7751577,7750219,7750691,7752036,7752145,7751839,7752185,7751848,7750242,7750950,7751988,7751166,7750585,7748490,7751256,7750807,7750911,7749919,7750884,7751248,7750980,7748487,7751070,7751302,7751634,7750148,7751496,7752024,7751489,7752110,7752050,7751970,7751226,7750328,7749684,7751337,7751838,7751993,7751809,7752179,7751928,7752000,7751612,7751807,7749800,7751026,7751392,7751513,7751793,7751625,7749840,7751740,7752198,7751840,7749804,7750329,7750450,7750688,7751831,7751932,7751500,7751275,7752039,7752027,7752189,7751836,7752175,7751643,7676983,7745826,7747210,7748460,3019094,3041908,3047490,3070903,3104580,3119714,4214716,4219933,4239825,3253155,3329577,3373246,3392269,3391784,3437845,3438895,3430445,3459922,3476733,3465573,3484602,3497723,3485458,3570190,3583401,3534554,3575540,3545325,3620341,3582530,3619677,3590352,3662878,3675915,3610888,3719454,3724098,3650408,3716837,3729237,3737662,4400616,4387439,3811082,3792965,3808058,3817408,3822830,3875223,3897450,3856649,3826778,3897333,3878085,3974878,4107010,6219060,6319034,6321949,6433213,4578913,4588093,4615076,4682285,4654912,4669463,4663826,4681696,4790772,4795478,4851843,4815342,4853861,4868323,4811302,4889135,4863297,4898691,4930297,4900239,4910855,4914319,4919962,4935350,4938756,4927937,4977154,4920723,4933466,4947874,4962196,5037816,5008555,5033931,5022422,5093397,5075939,5056369,5064653,5115368,5129164,5135638,5154706,5158751,5173531,5229749,5408544,5408960,5445860,5460545,5433463,5565794,5642407,5710242,5823360,5540685,5898013,5816707,6810040,6885854,6809498,6867450,7088974,7137195,7308968,7327536,7281550,7412215,5993310,5981349,6047175,6040025,6041091,7669801,7675429,7675255,7675212,7675539,7675171,7675190,7675434,7675438,7675649,7675373,7675228,7675271,7675354,7675275,7675460,7675517,7675596,7675172,7675699,7675359,7675338,7675577,7675560,7675522,7675603,7675843,7675519,7675530,7675678,7675323,7675541,7675670,7675307,7675242,7675305,7675378,7675416,7675651,7675215,7675465,7675471,7675574,7675610,7675679,7675260,7675203,7675294,7675329,7675433,7675494,7675723,7675311,7675589,7675764,7675485,7675310,7675389,7675653,7678683,7680459,7681085,7678573,7680976,7689176,7689695,7699885,7700372,7700978,7700851,7701954,7703530,7701204,7742840,7742673,7733460,7743234,7703771,7743824,7744297,7744227,7744499,7743271,7744953,7742375,7742683,7745663,7746140,7745856,7746237,7746697,7746797,7745079,7743343,7743482,7745271,7743553,7743872,7745036,7747309,7747440,7746289,7748056,7746707,7748634,7746143,7748817,7748973,7746063,7746168,7748587,7749703,7748693,7749981,7746779,7751317,7747537,7751693,7751599,7750882,7751792,7750874,7751090,7751860]
        progress_bar = tqdm(desc="Processing", total=len(website_ids))
        for website_id in website_ids:
            scrapping.delay(website_id)
            progress_bar.update(1)
        progress_bar.close()
