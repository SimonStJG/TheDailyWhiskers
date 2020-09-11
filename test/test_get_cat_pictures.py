import json
from pathlib import Path

from thedailywhiskers.dailywhiskers import get_cat_pictures, CatPicture


def test_get_cat_pictures():
    with (Path(__file__).parent / "sample.json").open("r") as f:
        top_cats = json.load(f)

    assert list(get_cat_pictures(top_cats)) == [
        CatPicture(
            url="https://preview.redd.it/mb9i7wiwe1m51.jpg?width=640&crop=smart&auto=webp&s=e3a25d474af9cdc225a79ba7168ef5d5ec7a27d5",
            reddit_url="https://www.reddit.com/r/cats/comments/ip817t/this_is_booker_booker_is_a_very_special_cat/",
        ),
        CatPicture(
            url="https://preview.redd.it/m959oft2y0m51.jpg?width=640&crop=smart&auto=webp&s=3f53339038dd3a3ffa97c130660f82a37f31b3ba",
            reddit_url="https://www.reddit.com/r/cats/comments/ip6jji/my_boy_turned_7_today/",
        ),
        CatPicture(
            url="https://preview.redd.it/5fqc3w33czl51.jpg?width=640&crop=smart&auto=webp&s=8aaa973677edd40708a72ccd12e1f54e17939702",
            reddit_url="https://www.reddit.com/r/cats/comments/ip0vwe/my_boyfriend_got_me_the_cutest_bday_gift_reddit/",
        ),
        CatPicture(
            url="https://preview.redd.it/k4cg80ef43m51.jpg?width=640&crop=smart&auto=webp&s=8d5db790410772de60eb223d4600257b02d58203",
            reddit_url="https://www.reddit.com/r/cats/comments/ipc981/this_kitten_is_affecting_me_on_a_molecular_level/",
        ),
        CatPicture(
            url="https://preview.redd.it/j14t68dy40m51.jpg?width=640&crop=smart&auto=webp&s=2477c67ed45e2372b8ce9b6c98092c331db74912",
            reddit_url="https://www.reddit.com/r/cats/comments/ip3vxp/am_i_dead/",
        ),
        CatPicture(
            url="https://preview.redd.it/4ibm6o4h71m51.jpg?width=640&crop=smart&auto=webp&s=d016e30e97963a05394cade9095a416de05f4eb3",
            reddit_url="https://www.reddit.com/r/cats/comments/ip7di8/my_little_photogenic_boy/",
        ),
        CatPicture(
            url="https://preview.redd.it/thu7jogqp0m51.jpg?width=640&crop=smart&auto=webp&s=1ff80146a5f4a1cda316ceb6d1675c344225f531",
            reddit_url="https://www.reddit.com/r/cats/comments/ip5smf/kitten_at_the_animal_shelter_i_volunteer_at/",
        ),
        CatPicture(
            url="https://preview.redd.it/qqcnuzzyf1m51.jpg?width=640&crop=smart&auto=webp&s=e66379d18398959322f6c4ecc9e3471449acb262",
            reddit_url="https://www.reddit.com/r/cats/comments/ip846c/we_found_three_kittens_and_a_skinny_nursing_mom/",
        ),
        CatPicture(
            url="https://preview.redd.it/fg1af30bkzl51.jpg?width=640&crop=smart&auto=webp&s=a3db1c1230f62468cc7e7636d6e432e5368a81b0",
            reddit_url="https://www.reddit.com/r/cats/comments/ip1shc/when_you_let_a_stranger_pet_your_cat/",
        ),
        CatPicture(
            url="https://preview.redd.it/5ynwpbbsm3m51.jpg?width=640&crop=smart&auto=webp&s=981695e95e189835bbf95c0d5926e41cf924d473",
            reddit_url="https://www.reddit.com/r/cats/comments/ipdd1v/this_is_navi_she_has_a_lot_of_ear_fluff/",
        ),
        CatPicture(
            url="https://preview.redd.it/50422sqq4zl51.jpg?width=640&crop=smart&auto=webp&s=8c5bb8461900962ea405fa2df9f5dd363b9ecccf",
            reddit_url="https://www.reddit.com/r/cats/comments/ip03gl/found_an_orphaned_kitten_near_a_busy_intersection/",
        ),
        CatPicture(
            url="https://preview.redd.it/3g44f6vevzl51.jpg?width=640&crop=smart&auto=webp&s=d7ddfebb46993c508cc84fd20118047e85291a5c",
            reddit_url="https://www.reddit.com/r/cats/comments/ip2y5g/my_handsome_man_is_missing_heres_a_cute_pic_of/",
        ),
        CatPicture(
            url="https://preview.redd.it/yrys9lx74yl51.png?width=640&crop=smart&auto=webp&s=b6d4b5b907dafa197382de53785fff3bc0015f85",
            reddit_url="https://www.reddit.com/r/cats/comments/iow4kh/a_small_boi_i_drew/",
        ),
        CatPicture(
            url="https://preview.redd.it/2f4ar98nf1m51.jpg?width=640&crop=smart&auto=webp&s=b76d64a5823214f2b9e65ffc2684f5ddae583b52",
            reddit_url="https://www.reddit.com/r/cats/comments/ip82ut/two_days_and_1700_later_my_murder_gremlin_is_home/",
        ),
        CatPicture(
            url="https://preview.redd.it/koc7nrs8u3m51.jpg?width=640&crop=smart&auto=webp&s=e62bcc98cb1ad51f809cdfddaa767f39eb2f305a",
            reddit_url="https://www.reddit.com/r/cats/comments/ipduc7/today_is_my_cat_chloes_birthday_today_she_turns_4/",
        ),
        CatPicture(
            url="https://preview.redd.it/o3oim3nvm0m51.jpg?width=640&crop=smart&auto=webp&s=7b525b2242864c155c60dc16fa4ece8e6abc2721",
            reddit_url="https://www.reddit.com/r/cats/comments/ip5jep/these_two_spend_all_day_fighting_then_give_me_10/",
        ),
    ]
