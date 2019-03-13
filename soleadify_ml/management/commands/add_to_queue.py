from tqdm import tqdm
from django.core.management.base import BaseCommand
from soleadify_ml.tasks import scrapping


class Command(BaseCommand):
    help = "Add to queue"

    def handle(self, *args, **options):
        website_ids = [3085326,7752223,7752214,7742321,7743640,7752207,7752215,7752297,4201050,5989364,7677019,7746430,7752299,7752243,7752221,3151869,5950525,7752287,7752202,7752301,7750068,7752233,7752209,7752290,7745563,7742393,7752239,7745655,7747580,7752254,7742641,7681967,5169021,7745187,7703039,6160173,7745589,7752303,7752238,7752240,7752292,7752259,7745762,4850658,7752260,7752306,3475324,7752312,6003434,7703480,7752285,7752274,7752264,7693318,3017579,7752268,7704412,7752218,7743561,7752269,7745335,3446126,7752271,3157559,3085589,7700329,5024348,7752224,3064142,7745483,7752226,7703289,7743517,3409540,5107113,7752236,7704310,7752228,7752231,7752219,3062450,7752289,7752277,7742579,7752296,7752232,7752272,7752278,7752307,7752204,7747806,3034539,7750979,7744637,7676031,7751646,4086912,7703635,7743382,7752234,7703097,7752206,7752227,7752275,7745658,7745489,7752237,7752244,7752298,7747357,7745458,7669790,7752257,7752315,5478703,7752225,7749681,7752242,7752261,5997536,7703703,7749809,7743130,7752229,3394325,7752253,7752262,7703638,7752258,3706642,7752300,7747356,7746899,7752282,6300973,3676904,7747598,3022009,4486992,7752273,7676086,7669762,4096750,7752245,7747851,7752305,7703643,6253448,3634401,7752283,7693127,7752249,7752279,7752252,7752205,7748240,7744797,6013605,7705138,4673842,7746280,7752251,7752316,3113672,7752294,7669820,4189511,7745868,5798998,7689250,7703840,5219775,3867406,7752250,7742436,5811282,7746201,7746578,7745639,7688863,7703377,7752311,6728770,3142939,7703732,7752288,7680016,7752263,4777929,7752265,7391229,4101524,7676430,7752295,7752291,7703749,7677130,7752302,7752304,7745890,7752281,7702590,7749246,7743466]
        progress_bar = tqdm(desc="Processing", total=len(website_ids))
        for website_id in website_ids:
            scrapping.delay(website_id)
            progress_bar.update(1)
        progress_bar.close()
