import scrapy


class LigaspiderSpider(scrapy.Spider):
    name = "ligaspider"
    allowed_domains = ["www.laliga.com"]
    start_urls = [
        "https://www.laliga.com/en-GB/laliga-easports/results"]

    def parse(self, response):
        for i in range(23, 12, -1):
            next_url = response.url + f"/20{i-1}-{i}"
            for j in range(1, 39):
                next_url_page = next_url + f"/gameweek-{j}"
                yield response.follow(next_url_page, callback=self.parse_gameweek)

    def parse_gameweek(self, response):
        matches = response.xpath(
            '//*[@id="__next"]/div[8]/div/div/div[2]/table/tbody/tr')
        for match in matches:
            if len(match.css('td')) != 8:
                continue
            link = match.css('td:last-child a').attrib['href']

            next_page_url = 'https://www.laliga.com' + link
            yield response.follow(next_page_url, callback=self.parse_match)

    def parse_match(self, response):
        basic_info = response.css(
            'div.styled__Row-sc-1gt2isc-0.gihJXq div.styled__ContainerMax-sc-1ba2tmq-0.esSirm')
        teams = basic_info.css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.dnFvYQ')
        Home_team = teams[0].css('::text').get()
        Away_team = teams[1].css('::text').get()
        scores = basic_info.css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.fLhOcF')
        Home_Score = scores[0].css('::text').get()
        Away_Score = scores[2].css('::text').get()
        temp = basic_info.css(
            'div.styled__BannerMatchRow-sc-1gt2isc-10.dUPnqe p.styled__TextRegularStyled-sc-1raci4c-0.gQuHhf')
        match_date = temp[0].css('::text').get().split(' ')[-1]
        match_time = temp[1].css('::text').get()
        stadium = temp[2].css('::text').get()
        if len(temp) >= 4:
            public_nbr = temp[3].css('::text').get().replace(',', '.')
        else:
            public_nbr = ''
        stats = response.css('div.styled__Stat-sc-a1enx8-1.lpPYC')
        possesions = stats[0].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        home_possesion = possesions[0].css('::text').get().replace('%', '')
        Away_possesion = possesions[1].css('::text').get().replace('%', '')
        total_shots = stats[1].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_total_shot = total_shots[0].css('::text').get()
        Away_total_shot = total_shots[1].css('::text').get()
        accuaracy = stats[2].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_accuaracy = accuaracy[0].css('::text').get().replace('%', '')
        Away_accuaracy = accuaracy[1].css('::text').get().replace('%', '')
        fouls = stats[3].css('p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_foul = fouls[0].css('::text').get()
        Away_foul = fouls[1].css('::text').get()
        yellow_cards = stats[4].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_yellow_cards = yellow_cards[0].css('::text').get()
        Away_yellow_cards = yellow_cards[1].css('::text').get()
        red_cards = stats[5].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_red_cards = red_cards[0].css('::text').get()
        Away_red_cards = red_cards[1].css('::text').get()
        offsides = stats[6].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_offside = offsides[0].css('::text').get()
        Away_offside = offsides[1].css('::text').get()
        corners_taken = stats[7].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_corner_taken = corners_taken[0].css('::text').get()
        Away_corner_taken = corners_taken[1].css('::text').get()
        penalties = stats[8].css(
            'p.styled__TextRegularStyled-sc-1raci4c-0.LfztD')
        Home_penalties = penalties[0].css('::text').get().split(' ')[0]
        Away_penalties = penalties[1].css('::text').get().split(' ')[0]

        yield {
            "match_date": match_date,
            "match_time": match_time,
            "home_team": Home_team,
            "away_team": Away_team,
            "home_score": Home_Score,
            "away_score": Away_Score,
            "stadium": stadium,
            "public_numb": public_nbr,
            "home_possesion": home_possesion,
            "away_possession": Away_possesion,
            "home_total_Shots": Home_total_shot,
            "away_total_Shots": Away_total_shot,
            "home_accuaracy": Home_accuaracy,
            "away_accuaracy": Away_accuaracy,
            "home_fouls": Home_foul,
            "away_fouls": Away_foul,
            "home_yellow_cards": Home_yellow_cards,
            "away_yellow_cards": Away_yellow_cards,
            "home_red_cards": Home_red_cards,
            "away_red_cards": Away_red_cards,
            "home_offsides": Home_offside,
            "away_offsides": Away_offside,
            "home_corners_taken": Home_corner_taken,
            "away_corners_taken": Away_corner_taken,
            "home_penalities": Home_penalties,
            "away_penalities": Away_penalties
        }
