"""
Cogstruction: Optimizing cog arrays in Legends of Idleon
    Copyright (C) 2021 Michael P. Lane

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import copy
import random
import numpy as np
import pickle as pkl
import time

from cog_array_stuff import get_excludes_dict, Cog_Array
from constants import ONE_SIG_PROB, EARLY_STOP_FACTOR

from coords import Coords
icon_data='iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABdWlDQ1BrQ0dDb2xvclNwYWNlRGlzcGxheVAzAAAokXWQvUvDUBTFT6tS0DqIDh0cMolD1NIKdnFoKxRFMFQFq1OafgltfCQpUnETVyn4H1jBWXCwiFRwcXAQRAcR3Zw6KbhoeN6XVNoi3sfl/Ticc7lcwBtQGSv2AijplpFMxKS11Lrke4OHnlOqZrKooiwK/v276/PR9d5PiFlNu3YQ2U9cl84ul3aeAlN//V3Vn8maGv3f1EGNGRbgkYmVbYsJ3iUeMWgp4qrgvMvHgtMunzuelWSc+JZY0gpqhrhJLKc79HwHl4plrbWD2N6f1VeXxRzqUcxhEyYYilBRgQQF4X/8044/ji1yV2BQLo8CLMpESRETssTz0KFhEjJxCEHqkLhz634PrfvJbW3vFZhtcM4v2tpCAzidoZPV29p4BBgaAG7qTDVUR+qh9uZywPsJMJgChu8os2HmwiF3e38M6Hvh/GMM8B0CdpXzryPO7RqFn4Er/QcXKWq8UwZBywAAAHhlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAABIAAAAAQAAAEgAAAABAAKgAgAEAAAAAQAAAECgAwAEAAAAAQAAAEAAAAAA+qOnAQAAAAlwSFlzAAALEwAACxMBAJqcGAAAAgZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIj4KICAgICAgICAgPHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjEwMjQ8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpQaXhlbFlEaW1lbnNpb24+MTAyNDwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgqiTJWwAAAVoUlEQVR4Ae2bCZSVxZWA3+uVbnYREURWRRGCC5EjMTpMolEYNIIimyibMOI2TnRiPCQSEx2jUYmaQ4SDC4Ii4HIGI2YmCeCWGDcwoqAGcAVRBKSh6fXN91X/9XyQllGbCGeSOqe6qm7dunW3urX8r1OpL5CmTJmSB3o6DknaNneCZTKZbDvi/n8os0KNHDnya6NGjequUBdffHGx5bnnnttnxIgRHa0nKYsfAftiuVsmhwwZkv/hhx8GnCVLllSfd95552LdKXl5eZ1ra2vfnTVr1sEKNXbs2MOAr6yuri5Pp9Nv1NTUjJ8zZ85z/fr1K7CfshZvqbW+r6XAYD1MpRE+b/78+TX2RUGo9mjcuHHnbdu2VeTn57fH6o8AW4zg59EWtbC0tLTX9u3b97eh0pIy0IhtYftKqs8DhGVkEAEnYdFD77nnnsuot6L+MNY/AQurmHRhYWGegldVVaUAaeEM7Xzq0/COScOHD9+/oKDgNuC/uvfee5caM/Y1T6hPAfCbSrHGf1JUVDQZoVOVlZWvAToQYVpibQU1GJpUhG3NH2G1KgalrAVWWFJSclB5eXktdIajyHn7mhJ2UkBkbvTo0Z1geE2doVOVGLWINZ9inStw8HXK3aUaPQH8FOPKUUgJClmDV3TZ3aC90RetFuZesWKFa7/k7rvvXoulb8EDFDpP9ya5LKLw1mvoq46Zdm6Qcxk4RlgR2fQf/pG+ira+L6RsEEQQjJ7WwuUyRr0rMEu9JK+usCe4fR7LQSMHgHh6CznEBoAKGIUUZurmHwJrOTkVvU3Y3kxhCURmDHow04p8EG47EbfNXe96QzXwAg1L/hN4L5G3kluTj6PvMHVAn9E/KjdoViWRJwNvSfnb2bNnP+42G3ca4HslFcCMRq7lENMSDqYStApxfyP7TsLTV11cXFxAQHyKMZcR1Z/P5VhhaA8k3453tIdGVEIafJdMmiX1U2iktm7deiLtx3v06JHRG/Zmykf4Avbn2mOOOebyRo0anbRjx45tWFBh4noPllf4iooK5L739Jdffvl9mR43btx+3bt3b9u3b187KpcvX76qZ8+eM+kagBLaQUf3dynoaRmXCIqthFZHhH/y1ltvXa3iXn311bDtgvOVJ5nT0gq5DOE3oZDGNHN3hxrdHuGfQ8hzxWV/b8NymYUwryPoCsaton3NhAkTCjkBfgJsAA6wFVruBFE4mmmOEXmN8KIVgN+Tll5gubdSOJh40mOLehSm+sOkvOQqoA6QTn/fDg83KORpvGUUuMaLRgjVnhPgD1HEXHHuvPNOPeR6dxFwXAqmWqXHK9Yztg8xYJXWJ/4EA9ShfPV/Q6Ru3bp1sAJRvSJRQLRKLbA8rPk6TD8lewj/Y+pdEbY8sW4GoWo5/lYAH3zOOeeMFA9ZHwJHOoXkSM+u/E2bNlVYmTdv3l4VXh7C+jQSjxkzpjVyfK8eBYj32vTp06uwWBFCn4oLC/MWqHeY84C79yv4GbRTWP9taL2dbJUqQOvrBa0JtFewXErpF57rbQ79SpMKyHDyOwrmN7B2z8HaWiUEQISKzGy3wkVIpkut07cT48Bju5n9pCpysHRo1f1RCRmU8594xwpukU0B71UlhCUAEzXyj/A7qEdBwiFIJZDbyj8nxM0Ub2FFm/GAYz2sdeHgrrTNVtecolUyPksTWE3iQUXgxPjgkC+b0p5j4uCknjtf7Kq3rJOkpuYDGHV7agSWg6PpXf8K13v8+PFtpICQU/EUYY6tYpxCVNIuZqcQ5Vf+wfWPBq8VFle5kSEvRQUETFE2sPQ8debOJ/xzp0TYDKVe63lDZVgXllXK7ggGpK5du34EY9/ALceAXJYwHFwTATwANcVq4ySEF8wFbwrC5QEvJBeQvSypiMFsla+Jh6IuTeSOygwBFSZXEjAHgD9MvC+aEsFUWhCWuNSEF6r2tD3RZQjCbVnSLaJSErzPVEa0TJYP9vOZrNGxWLMagh5n4xqF59pj2b5eFJlJjkOYs8gHkN8khsy+7777VtvHVXoCNO7gnOAyifEknCShOwElzRDPcwPBVcUFJUFH3UeFibJTcrvOfVRhngvBvxEkj+NHsAt9gnFWQedg4FeztV8XCew6NsLjeV2BGmFdY8ATDB6bw4hKCns45WIUdAaEF4P7R9rmnZJM4f63I7zwrOahF5YTSsyOcWcRKborOD6d5Xkr3fWOIJxcDZ+dWJYVGGIdQ09C6BKUWoLQLyG8RuuMR6aAnUL/deM4rWKcVvD7RkLDJZJNwQNiB8QPh8HfQuQgCGatl2DX4NbBmhCcQ30WOCsRdDvWNuD1Jl/A0uin8PQFcyZjtapvBAWMfYo8nPPEIaAMYj5fi8KycSu+6667PkzGyFvwhhz+TgB/EXCFf5kctlxKl1y4sUI7CqjyHyV3JB/BXKczz2ORFrCQggeocVsgdUN7B6G9Sui5riVmnznftnKBM5LqSCyxHUE8EDVFCZ4RvESF8z9KDDQZJw358+JFNdUbRSwi99RSZWVlbYANw3O6w/wzlE+CexmvR38BLo3Ms88+62GqgjnPZ0xj4tEhKjDZTejyAlobDifUNVIwFDgDoZkyaIPrTfcxZFXmiFvnorqba4RJ/wvhZxClFX6dXCeCBM4ZGLQMDrJXG91LQfE4XMQE1YnwTp4VHkG1hAyuoa4mBqOIZ9UPwnu+GMqyeov20/S1wKVPo/8PKMI7Scbj8qJFi8L2As4D0NFQTFdp7FC5elaeBjAhrPMLr5UfcONZZD4w3yMqgUX+6jRlx9q1a4OQXE500Zd4xzsfYh/A1L8wQBSTA+EjbIEK5jFYgH1OnF3zjMkw1oPPDnI/+g6k1L03kS/XMowrVinM05w+1/EOhvjesAB3nW+QpKxGQQOPOuqob9N/FWMMuoEP6TPW2PIa9P6HvJyx0juQOcI1HFwtbv3IXr16VUOn4+DBg191KRBQP9UESCYJZ6UVwORXodhrE40roFqFj3SupUV1ebjPO94+GfFx9DhgeVj2GYJUfDD1TuFyKQdtFbkpuF0TpeguyzHAN7FWGXGpBe01HJ9b4Hn2ST8q9xPq4wjKCyizCZ7707gb5R4AzeySdMnJA7IcPHfu3PdVQnYXSEZLPM1yyOeC5HcBDzhtULTdfgtorFAIKvMh0IlP2+fwYA3wXW/2lYPrY2hnYFc4hhzcEnghODMZexUW3qCbI+B3aN8DbmtoHUn7FQTxDWEesAwKoTu4tkbSs1yC32LZvsDefwI8jgLu+8YDwBYBO572S7SbJEqrdZcArwjlH07f+8a+rMsCiCmT7LVqTo2vYfJq4kJjmPkjjE8kL0CYLXTLTBVE0+C9B3wGeRJ96xGghAk3wsBHjPse1gvvA0zui9MDCD5e4bUCiq7Fikb3U6ATvjEwriNzdlIA6A/WY0gayPOEyrxJ4YkV/0r7Cbz0fPJY8m/4gvUDtsk3wb0mGacsGerGtnHM+3tjHvPW1KcAcEOwqJE5kKfCRFe+Bt0CI4OYdDrMDgF2ITJ65C0ky9DJwCfQP41JzkRp1zVv3vwgYL7/LYHkYhhI6zmkcEBxjTOHASvjN0Zwtdh8hNDC7i7i9qTexIoJWIE0wJuj51DeoJcDq0D5JnF+Oq5u/7+ftutVT3d52ud82bTrEsh2WJE5J4Gxt2n+uzAZve222zBoxWKI/QFQC8pXUdRKcWnnI/AzlGZp5K1Zs+ab4PRFEEEfk8NrUHIKFJZq1apV8Diqr9lGqSUcmY3cetEcvEawT0p6WyXtd4gr3Wk3pe3YYhGoh4dblNKL16mlLKPN4LQEnp8o7pd4TWf4vVp6u1WABHUThaDqSaxG4R1oEKH8BjmbxKUR8NlVijh97Vi9evUwGJ3Dcoifz/YDx61zo7EmWW6pjRs3qrxqGO2EstwuvZ1eSjm1adOmzbg5und71tCibnetEfJt6rqU68OLGc203mMcWsPrlfM0kR7J2FWF15binSNpX4089cYAkXdKIHpE1QSBUlLGa2gss2PEZ8kEX4fJN3RLGLO/Bve2vMg/Cu9adCmoWC814J2VLBOVMB60pQj/PnAHIkMm0KA8Awu7C9zsUjSwkrxpqoAZ3Eveon068xXSlneXQCHCr2PsTNopg2DgysbfIEk7XEvxgleod4SBUibXvbXuZNzw2jgvbtmd/gfp80QYDi88wBRzWDoTvIdw5dX0dabPSO5ZQdfujpetNxBCZxTjtbJniJtQailetwqc9iogGbMBb+zG0tuCkcJ76N9SAVG2FFtS25YtW368ZcuWK7HUFIT3pdk1uRak5WS/SZyoYmA2nBFg2D3b3xp8XUujgEcY813GaM00dPKh8yZ4g1HCn4FlE7tAV+g8CP6RzmVHgv8M8ex4vS4uva9CAcETZAIhOlC8KT/kKpgqwmr6tR4RFjD1v5B/Rv8oytsJqPMQ6EyEWeDSEJfkH98XwjskNBYC95apm3+d+hmJwAofnuaB+xTnwWyiO1lUwv8ZBCHQ0OR5vogA6Rl8GAGtELf2el0EMz6+GKS8xspsMfDhWPQ56jPixFjzSeLIG7TbkJuB407gR9sgIMo5jfGniQ+tcBBLLO82aSxJiwuN7dT/WzwUUIsXfHp2F7inU7LOVHJwQ5iZifDXw7CBymdz3wy1bgHWKTZAwmd4L5MXPMYonmJNbwDvZsZfQXM0Yw2w0XurEKwKWtVm6/SZTQwLJ9CLGNsJ4U9AuWvj+hchErG+J1OkG3eN+PoTGON8fyDMbOMDylYnJYjdDoNerLyNLm3SpImXo8kwfz55KO68DMU8xYmvA/3zGNIBpR0Hjms7HMuph7mg4zdIl1TwBuBvsu4PjcLlCi8sMhr7G1zmToAFu0FwMrkMJiYRDA9D8OkINRtr3elkydnBajYx7rtsbY+AEw42Kofk93hdfyWIL1IfgVIW07cK2CDKNiJR+nL9INWO7CInsx0/CZ1TmKfcg9qu833mUTjLzeevBGWigNoxvOwkwwY2a9ZsFEJfgJVnU85lnz5RJdBvXKgZW/dtIPtzO8ch0Fr263C7xOoYuaAQq3oKtPswcgnCezt6mIB2AUKfpdURWB7GoOzzKQdBYyjL50SFp/1Xz2zA9qgHOHmGiP0jtH8Z9XvJPlkdTK6GQZ/DXOPeMD3RPUpJkTmaPAhGn8fyZ4E7mnwIQh+mG5N+nuB65P43XL8fpXBplYnnt0i9BlAhSnq0U6dOlRoiINX9CbzltLPVYLVs68tXAh2s7Jej12GyHWVYh1jT9wNdU2k0oduSLzi6s5/QUljqZ1jtSoR4ivV/PIEyHJbYJc5jG5yVyxY4v8b9B6hM0krq3+Ed8Z1cHKej7TG7YOnSpbsqIxc17Mc7Ab5kI5gEK27DA/z03Q7mPc1hkDz0UWhAKlAplG5TGfoNiBmsrDf8KZm3gguQg7TuMoVnuwpbNVYtIILvAD6F/gEILq1BifDhLiANjrcemasShQcXAo9m/c/teyIGBOtjmankZ5j8ZIRSIXhngefwDQh8DXkAEXwY+UEEkCGZjgeZaXjP72D0GvJM4oR3h7X0p7p165bGktUIGo7H9G+AZviKTf0iApsv0l6ERpAv50nPJUY1M4vsLrJf0g58SjM3NUgByfU3g+B9iNqXInBfZ2aCWuoeVZ/GvdsRqK7G1V+k/jBe4seUgWRPbeGlGfwDCJbfopzisnDt099b6/vtwIMUgTVcd7F8bzyqGJyy/fff/0JukReBexNj55BvpK4SXTajyAbbi8mmeg999WqlDv9z/XV8ZhyPD3j0XVj2dFw0XDxgwstKW7ahUpTzO4Q9CpjPWL7kfJ+lcgmC/AKPiBcVH2C3obgu0NpOWYqQdxEbxkZO2DG6AFuCEg6GTorfMacWLlzoN4wLwbmKbLQvSfB9cfZQ9SNwf5LA/qpoqAJS/fv3L/bZmj1+JK7r/l7O1uXXmttg/hKXBQroi/VdjwXUDXpD6FtA32aYa64wWP5d8kCUsMzAaJCj7iHHff83CCneEBTjd4Ey5vohN77hRxxxxAJoXgJO+0S61ymNLz2StopYQvZT/CnQ8KWJoi4mNGgJeOhReKx5NszegNDMkcr3DxO8lPyUvjeBzWUh3Jccu0/3D+ktg1niNe2h8QNg1xsvgN0jLrDDucJeyh1iNH2NxX/nnXeeuOOOOx7v3bu3S+8G4AqvoGeSD2funpTHkd8i6wUDyCeQ43IIPNJu8F0gKBDLyWA7NFtBjrDWyevRFqymp1WSa6g771r/kJqBr7LcEmu4Mg9F4N/jHYuA344nhV0Dr9rE1uhnru0GSJbVgeSJEkCz2yxJkyDzEKUR0EvQs9Q9V5j0CHM4elNqkJAa5AFsOYEQTN/Mq82fKYuZ2KdshRqSzHGlVsOti7FWCe7/bpcuXabgNX4i6wSuBxYtUsNvh+6nfMNx9JUh+K8RxhPhVSjFL0aXbN68+W6CY3/OC5ehtJvQbGPQPyYvdFySHOO2+zztF8juONfSngbcK3g4RIjb4BgQz9dG7A4dOqxHCa10aQQuwIWvIOD9nLV+NHMNZfL17AJTnRjYMrzBB4sKLO2PK0LMsM+lRQ4nOX+Vtm7dus1shTKdtZx40BtOcR/Z8/+hCPYRMJUZlErb3zK/TPtr5MXkkcB8EqOoiwH1bg0gfu7k7/w4a6fat2/fi0Fec93ewvM3VrwRQTsz4Y8R/EqJst//E92/RPgeCK9Q4bM5OO1Upr8co18Lps8+++y8+++//yPHmVRMnz59CgcMGOBSG4Q2ZmNBI38L8gjyrYyN1lX4bwNTeOPDP4M/g3IgWc8PeA1WAJaRmA8cx+KWLQ2ELgEVQenVdBJBbRKKeA+8Rmx9/mzGvT4Ij5Lyk6h/Kv1Get2ZIlhInOil4acwCBWiKPCP6HDuuO3dQp/4s8mWJ5Fnkk0GQgk9YEmKND+t1MEb9pd1PRkK22DkCgRomzBk8PEjqMFJxdjWlb3ean1Phi8AfwUvWRiXFP2fmaDjUVIvmQaSCjiefEgyYCOl21G7pO3yuJSsUryAbWEcRd0SyGoiQd4jBYoYg6XvxPLhsuOxn0llwMfM8IkdwYVt9OtRslsEF49r/4swAp3+4D9GLiM3ScbqKXr4kwh7YgJzzqzwwhq0C0SisYz/QsckurHpbZQwm7ZWcGvS4suAzXU7pP3B+vXrC13bWv6LCg/dojALSyspFX4BeRjZbwam7eD54wzzTsLXde/hv04iSdZ8HzwhnMaoD5w4caJ3Bk9pIREMT0l+om+7QZ6YCOePtqaSW0mQ8lSi4FDrJtoNmqOOyuf8q0UjqpZ1ixw9evSxCNxFOP26Zkx7nDGEDRenOMFeKROXzioih4kgsP3A9pjwCO1DS3Bz54rtnHn3bnU3Ctm7jP1j9n9o4O9bA/8L2R1fntS0H1YAAAAASUVORK5CYII='

"""
- This singleton controls the loops of the genetic algorithm. 
- It also controls if the genetic algorithm should do a cross breed or a one-point-mutation.
- It also prints status info.
"""

class Iteration_Controller:
    def __init__(self):
        self.best = None

        self.num_restarts = None
        self.restart_count = 0

        self.max_generations = None
        self.min_generations = None
        self.max_running_total_len = None
        self.req_running_total = None
        self.curr_running_total_len = 0
        self.curr_running_total = 0
        self.generation_count = 0
        self.previous_best_improve = 0

        self.orig_pop = None
        self.curr_pop = None

        self.num_mutations = None
        self.mutation_count = 0

        self.prob_cross_breed = None
        self.prob_one_point_mutation = None
        self.prob_two_point_mutation = None
        self.cross_breed_count = 0

    """
    `num_restarts' in the number of random restarts.
    """
    def set_restart_info(self,num_restarts):
        self.num_restarts = num_restarts
        return self

    """
    Sometime between `min_generations' and `max_generations', the algorithm will begin looking for a reason to terminate 
    the generation loop. It will look at the previous `max_running_total_len' generations and if the percent improvement 
    from the original population is in excess of `req_running_total', then the the generation loop will continue. If not,
    it will cancel before it hits `max_generations'.
    """
    def set_generation_info(self,min_generations,max_generations,max_running_total_len,req_running_total):
        self.min_generations = min_generations
        self.max_generations = max_generations
        self.max_running_total_len = max_running_total_len
        self.req_running_total = req_running_total
        return self

    """
    - `num_mutations' is how many mutations to do per generation.
    - `prob_cross_breed' is the probability of calling `Cog_Array.cross_breed'; likewise `1-prob_cross_breed' is the
    probability of calling `Cog_Array.one_point_mutation'.
    """
    def set_mutation_info(self, num_mutations):
        self.num_mutations = num_mutations
        return self

    def set_breeding_scheme_info(self, prob_cross_breed, prob_one_point_mutation, prob_two_point_mutation):
        self.prob_cross_breed = prob_cross_breed
        self.prob_one_point_mutation = prob_one_point_mutation
        self.prob_two_point_mutation = prob_two_point_mutation
        return self

    def set_pop(self,pop):
        self.orig_pop = copy.copy(pop)
        self.curr_pop = pop
        return self

    def mutation_loop(self):
        if self.mutation_count >= self.num_mutations:
            self.cross_breed_count = 0
            self.mutation_count = 0
            return False
        else:
            self.mutation_count+=1
            return True

    def generation_loop(self):
        if ((
                self.generation_count <= (self.max_generations - self.min_generations) * EARLY_STOP_FACTOR + self.min_generations or
                self.curr_running_total_len <= self.max_running_total_len
        ) and self.generation_count <= self.max_generations):
            if (
                self.best_improve_from_original() - self.previous_best_improve + self.curr_running_total >= self.req_running_total or
                self.generation_count <= self.min_generations
            ):
                self.curr_running_total = 0
                self.curr_running_total_len = 0

            else:
                self.curr_running_total_len += 1
                self.curr_running_total += self.best_improve_from_original() - self.previous_best_improve
            self.previous_best_improve = self.best_improve_from_original()
            self.generation_count+=1
            return True
        else:
            self.generation_count = 0
            return False

    def restart_loop(self):
        if self.restart_count < self.num_restarts:
            self.restart_count+=1
            return True
        else:
            return False

    def breeding_scheme(self):
        rand = random.uniform(0,1)
        if rand >= 1-self.prob_cross_breed:
            return "cross_breed"
        elif rand >= 1-self.prob_cross_breed - self.prob_one_point_mutation:
            return "one_point_mutation"
        else:
            return "two_point_mutation"

    def print_restart_status_open(self):
        print("Restart:                              %d" % (self.restart_count-1))
        print("Pop size:                             %d" % self.orig_pop.get_size())

    def print_generation_status(self):
        if self.generation_count % 10 == 1:
            print("\tGeneration:                             %d" % (self.generation_count-1))
            if self.generation_count >= 11:
                print("\t\tMax improvement from original pop:    %1.3f%%" % ((self.best_improve_from_original()-1)*100))
                print("\t\t90th %%ile improvement from original: %1.3f%%" % ((self.perc_improve_from_original(0.90)-1)*100))
                print("\t\t50th %%ile improvement from original: %1.3f%%" % ((self.perc_improve_from_original(0.50)-1)*100))
                print(self.curr_pop.get_best()[0].str_with_abbr())
                # print("\t\t%% cross-breeds:                      %d%%\n" % int(100*self.cross_breed_count/self.mutation_count))

    def perc_improve_from_original(self,perc):
        return self.curr_pop.get_percentile(perc)[1] / self.orig_pop.get_percentile(perc)[1]

    def best_improve_from_original(self):
        return self.curr_pop.get_best()[1] / self.orig_pop.get_best()[1]

    def print_restart_status_close(self):
        if self.restart_count == 1:
            self.best = self.curr_pop.get_best()
        else:
            self.best = max([self.best, self.curr_pop.get_best()], key=lambda t: t[1])
        print("Best so far:                          %.4f" % (self.best[1]))
        print("Build rate:                           %d" % self.best[0].get_build_rate())
        print("Flaggy rate:                          %d" % self.best[0].get_flaggy_rate())
        print("Exp mult:                             %d%%" % (100 * self.best[0].get_total_exp_mult()))

    def print_init_info(self):
        print("NUM RESTARTS:   %d" % self.num_restarts)
        print("MIN_GENERATION: %d" % self.min_generations)
        print("MAX_GENERATION: %d" % self.max_generations)

"""
- A population of `Cog_Arrays'.
"""
class Population:
    def __init__(self,arrays,obj_fxn):
        self.arrays = arrays
        self.obj_fxn = obj_fxn
        self.values = list(map(self.obj_fxn,self.arrays))
        self.is_sorted = False
        self.pop_size = len(arrays)

    def add(self,array):
        self.arrays.append(array)
        self.values.append(self.obj_fxn(array))
        self.is_sorted = False
        return array, self.values[-1]

    def cull(self,pop_size = None):
        self.sort()
        N = self.pop_size if pop_size is None else pop_size
        self.arrays = self.arrays[:N]
        self.values = self.values[:N]

    def sample(self,k=1):
        return random.sample(list(zip(self.arrays,self.values)),k)

    def get_best(self):
        return self.sort().arrays[0],self.values[0]

    def get_mean(self):
        return np.mean(self.values)

    def get_median(self):
        return self.get_percentile(0.50)

    def get_percentile(self,perc):
        self.sort()
        i = int((1-perc)*self.get_size())
        return self.arrays[i],self.values[i]

    def get_perc_std(self):
        return self.get_percentile(0.50 + ONE_SIG_PROB)[1] - self.get_median()[1]

    def get_z_score(self,other):
        return (other.get_median()[1] - self.get_median()[1])/self.get_perc_std()

    def sort(self):
        if not self.is_sorted:
            sorted_pairs = sorted(zip(self.values, self.arrays),key=lambda t:-t[0])
            self.values = [v for (v,_) in sorted_pairs]
            self.arrays = [a for (_,a) in sorted_pairs]
            self.is_sorted = True
        return self

    def get_size(self):
        return len(self.arrays)

    def __copy__(self):
        return Population([copy.copy(array) for array in self.arrays], self.obj_fxn)

"""
The genetic algorithm.
    - cogs: A collection of all cogs in the user's inventory, including characters. `cogs' excludes any characters that 
    the user intends to place on the cog shelf.
    - empties_set: An `Empties_Set' of all `Coords' that the user has not unlocked using flaggies. `empties_set' 
    includes all `Coords' where the user currently has flaggies placed.
    - flaggies: A collection of all `Coords' where the user currently has flaggies placed.
    - pop_size: The initial population size. This is also the population size after each mutation loop terminates.
    - obj_fxn: The objective function, takes input `Cog_Array' and outputs a positive `float'.
    - factor_base: A float greater than 1. A smaller float corresponds to smaller `factors' passed to 
    `Cog.update_strengths', a larger float to larger `factors'.
    - max_factor: See `Cog.update_strengths'.
    - max_multiplier: See `Cog.update_strengths'.
    - controller: A singleton of class `Iteration_Controller'.
"""
def learning_algo(
        cogs,
        empties_set,
        flaggies,
        pop_size,
        obj_fxn,
        factor_base,
        max_factor,
        max_multiplier,
        controller,
        window
):

    controller.print_init_info()

    excludes_dict = get_excludes_dict(empties_set,cogs)
    #print("emp.\n",empties_set)
    #print("dict\n",excludes_dict)
    cog_array_template = Cog_Array(empties_set,None,excludes_dict).extend_spares(cogs)
    cog_array_initial = copy.copy(cog_array_template)
    for cog in cogs:
        #print(cog.precoord_x,cog.precoord_y)
        if(cog.precoord_y is not None):
            cog_array_initial.move_cog_from_spares(Coords(cog.precoord_x,cog.precoord_y),cog)
    #print("template\n",cog_array_initial)

    can_do_one_point_mutation = cog_array_template.get_num_non_empty() < cog_array_template.get_num_spares()

    bests = []
    # with open("hello.pkl", "rb") as fh:
    #     cogs = pkl.load(fh)
    average_std_objs = {}
    for i, cog in enumerate(cogs):
        average_std_objs[cog] = cog.get_average_std_obj(cog_array_template, obj_fxn)
    # with open("hello.pkl", "wb") as fh:
    #     pkl.dump(cogs,fh)
    # raise Exception

    while controller.restart_loop():
        for cog in cogs:
            cog.instantiate_strengths(cog_array_template)

        pop = []
        for _ in range(pop_size):
            cog_array = Cog_Array(empties_set,None,excludes_dict)
            cog_array.instantiate_randomly(cogs)
            pop.append(cog_array)
        pop = Population(pop,obj_fxn)

        controller.set_pop(pop)
        controller.print_restart_status_open()


        while controller.generation_loop():

            controller.print_generation_status()
            window["-PROG-"].update(controller.generation_count-1)

            while controller.mutation_loop():

                breeding_scheme = controller.breeding_scheme()
                if breeding_scheme == "cross_breed":
                    (array1,_),(array2,_) = pop.sample(2)
                    pop.add(array1.cross_breed(array2))

                elif breeding_scheme == "two_point_mutation" or not can_do_one_point_mutation:
                    old_array,old_obj = pop.sample(1)[0]
                    new_array, coords1, coords2 = old_array.two_point_mutation()
                    cog1 = old_array[coords1]
                    cog2 = old_array[coords2]
                    _, new_obj = pop.add(new_array)
                    try:
                        prop_new = new_obj / (old_obj + new_obj)
                        factor = factor_base ** ((prop_new-1/2)*old_array.get_num_occupied())
                        cog1.update_strength(coords2,factor,max_factor,max_multiplier)
                        cog1.update_strength(coords1,1/factor,max_factor,max_multiplier)
                        cog2.update_strength(coords1, factor, max_factor,max_multiplier)
                        cog2.update_strength(coords2, 1/factor,max_factor,max_multiplier)
                        pass
                    except ZeroDivisionError:
                        pass

                elif breeding_scheme == "one_point_mutation":
                    old_array,old_obj = pop.sample(1)[0]
                    new_array,coords,old_cog = old_array.one_point_mutation()
                    new_cog = new_array[coords]
                    _, new_obj = pop.add(new_array)
                    median_diff = average_std_objs[new_cog][0] - average_std_objs[old_cog][0]
                    std_diff = np.sqrt(average_std_objs[new_cog][1] ** 2 + average_std_objs[old_cog][1] ** 2)
                    try:
                        z_score = (new_obj - old_obj - median_diff) / std_diff
                        factor = factor_base ** z_score
                        old_cog.update_strength(coords, 1 / factor, max_factor, max_multiplier)
                        new_cog.update_strength(coords, factor, max_factor, max_multiplier)
                        pass
                        # if (
                        #         (
                        #         new_cog.__class__.__name__ == "Up_Cog" and
                        #         coords.y == 7 and
                        #         np.max(new_cog.get_strength(coords))>=0.03
                        #         ) or (
                        #
                        #     )
                        # ):
                        #     print("NEW")
                        #     print(new_array.str_with_abbr())
                        #     print("OLD")
                        #     print(old_array.str_with_abbr())
                        #     print("new_cog:                      %s" % str(new_cog).replace("\n","\t"))
                        #     print("new_obj:                      %1.5f" % new_obj)
                        #     print("old_cog:                      %s" % str(old_cog).replace("\n","\t"))
                        #     print("old_obj:                      %1.5f" % old_obj)
                        #     print("Coords:                       %s" % coords)
                        #     print("average_std_objs[new_cog][0]: %1.5f" % average_std_objs[new_cog][0])
                        #     print("average_std_objs[old_cog][0]: %1.5f" % average_std_objs[old_cog][0])
                        #     print("median_diff:                  %1.5f" % median_diff)
                        #     print("average_std_objs[new_cog][1]: %1.5f" % average_std_objs[new_cog][1])
                        #     print("average_std_objs[old_cog][1]: %1.5f" % average_std_objs[old_cog][1])
                        #     print("std_diff:                     %1.5f" % std_diff)
                        #     print("z_score:                      %1.5f" % z_score)
                        #     print("pre_factor:                   %1.5f" % pre_factor)
                        #     print("new_cog factor:               %1.5f" % factor)
                        #     print("old_cog factor:               %1.5f" % (1/factor))
                        #     print("new_cog.get_strength(coords): %1.5f" % new_cog.get_strength(coords))
                        #     print("old_cog.get_strength(coords): %1.5f" % old_cog.get_strength(coords))
                        #     print("new_cog.strengths:\n%s" % np.array2string(new_cog.strengths.transpose(),precision=5,max_line_width=120))
                        #     print("old_cog.strengths:\n%s" % np.array2string(old_cog.strengths.transpose(),precision=5,max_line_width=120))
                        # elif (
                        #     old_cog.__class__.__name__ == "Up_Cog" and
                        #     # old_cog.build_rate == 28 and
                        #     # old_cog.exp_rate == 0.07 and
                        #     # old_cog.build_rate_boost == 0.09 and
                        #     coords.y == 7 and
                        #     np.max(old_cog.get_strength(coords)) >= 0.03
                        # ):
                        #     print("OLD")
                        #     print(old_array.str_with_abbr())
                        #     print("NEW")
                        #     print(new_array.str_with_abbr())
                        #     print("old_cog:                      %s" % str(old_cog).replace("\n","\t"))
                        #     print("old_obj:                      %1.5f" % old_obj)
                        #     print("new_cog:                      %s" % str(new_cog).replace("\n","\t"))
                        #     print("new_obj:                      %1.5f" % new_obj)
                        #     print("Coords:                       %s" % coords)
                        #     print("average_std_objs[old_cog][0]: %1.5f" % average_std_objs[old_cog][0])
                        #     print("average_std_objs[new_cog][0]: %1.5f" % average_std_objs[new_cog][0])
                        #     print("median_diff:                  %1.5f" % median_diff)
                        #     print("average_std_objs[old_cog][1]: %1.5f" % average_std_objs[old_cog][1])
                        #     print("average_std_objs[new_cog][1]: %1.5f" % average_std_objs[new_cog][1])
                        #     print("std_diff:                     %1.5f" % std_diff)
                        #     print("z_score:                      %1.5f" % z_score)
                        #     print("pre_factor:                   %1.5f" % pre_factor)
                        #     print("old_cog factor:               %1.5f" % (1/factor))
                        #     print("new_cog factor:               %1.5f" % factor)
                        #     print("old_cog.get_strength(coords): %1.5f" % old_cog.get_strength(coords))
                        #     print("new_cog.get_strength(coords): %1.5f" % new_cog.get_strength(coords))
                        #     print("old_cog.strengths:\n%s" % np.array2string(old_cog.strengths.transpose(),precision=5,max_line_width=120))
                        #     print("new_cog.strengths\n%s" % np.array2string(new_cog.strengths.transpose(),precision=5,max_line_width=120))
                    except ZeroDivisionError:
                        pass

                else:
                    raise RuntimeError("Breeding scheme must be among `cross_breed`, `one_point_mutation`, and `two_point_mutation`.")
            pop.cull()
            #print(pop.get_best())
        controller.print_restart_status_close()


        bests.append(pop.get_best())
    """
    popup_str_initial="\n".join([
                    f"Build rate:\t{cog_array_initial.get_build_rate():,.0f}",
                    f"Flaggy rate:\t{cog_array_initial.get_flaggy_rate():,.0f}",
                    f"Exp mult:\t{100 * cog_array_initial.get_total_exp_mult():.0f}%"
                    ])       
    #print("initial\n%s"%popup_str_initial)   
    popup_str_final="\n".join([
                    f"Build rate:\t{controller.best[0].get_build_rate():,.0f}",
                    f"Flaggy rate:\t{controller.best[0].get_flaggy_rate():,.0f}",
                    f"Exp mult:\t{100 * controller.best[0].get_total_exp_mult():.0f}%"
                    ]) 
    print("final\n%s"%popup_str_final)
    """
    popup_str_diff="\n".join([
                    f"Build rate:\t{controller.best[0].get_build_rate():,.0f}\t({controller.best[0].get_build_rate()-cog_array_initial.get_build_rate():,.0f})",
                    f"Flaggy rate:\t{controller.best[0].get_flaggy_rate():,.0f}\t({controller.best[0].get_flaggy_rate()-cog_array_initial.get_flaggy_rate():,.0f})",
                    f"Exp mult:\t\t{100 * controller.best[0].get_total_exp_mult():.0f}%\t({controller.best[0].get_total_exp_mult()-cog_array_initial.get_total_exp_mult():,.0f}%)"
                    ])    

    #print("final\n",popup_str_diff)
    window["-T-RES-"].update(popup_str_diff) 
    #print(res)

    window["-PROG-"].update(controller.max_generations)
    #print("Best so far:%.4f" % (controller.best[1]))
    #print("Build rate:%d" % controller.best[0].get_build_rate())
    #print("Flaggy rate:%d" % controller.best[0].get_flaggy_rate())
    #print("Exp mult:%d%%" % (100 * controller.best[0].get_total_exp_mult())) 
    #print(bests[0][0])
    #print(pop)
    return max(bests, key=lambda t:t[1])