<div width=100% style="text-align: center; margin: 0; ">
<img src="dealHunter2.png" alt="MarineGEO circle logo" style="width:30%; border: 2px solid #1e1e1e; border-radius: 10px; "/>
</div>
<br>


# Project description #
<span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**dealHunter&reg;**</span> is a web service designated for people, who want to buy a certain product (currently we support cars from slovenian website ***Avto.net***), but don't want to spend <span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**to much time scrolling**</span> through endless pages of what is avaliable on the internet. ****dealHunter**** provides a service, that enables users to filter what kind of product they need and after that <span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**we take care of everything else.**</span> Our users can just relax and wait for an email notification, signaling them it's time to buy their dream car, or maybe a house, who knows of <span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**all the fields we could expand to.**</span>
<br>
<br>
<span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**Our mission**</span> is to help people put their valuable time to better use, while at the same time not missing on great deals &rarr; ****dealHunter**** always hunts for them. We believe that our project offers <span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**great scaling possibility,**</span> as such service could be used across many <span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**different parts of human endeavors,**</span> for example searching for an apartment, buying a new TV or laptop...

# Code description #
<span style="color: #142b65; background-color: white; border-color: white; border-radius: 3px; padding-left: 3px; padding-right: 3px;">**dealHunter's**</span> architecture could be divided into four subcategories:

&nbsp;&nbsp;**&rarr;** <span style="color: white; background-color: RGBA(194, 193, 194, 60%); border-color: white; border-radius: 3px; padding-left: 6px; padding-right: 6px;">**HTML&CSS user interface:**</span>
<br>
<span class="tab">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;****dealHunter's**** user interface is in a website form, written from stratch using _HTML_ and _CSS_. It has quite a retro style **&rarr;** you could sense that we come from FMF from afar. Webpage is divided into a welcome page, an empty _"Nepremičnine"_ page and a fully working _"Avtonet"_ page. The latter enables user to set parameters and then submit a subscription to our notification service</span> 
&nbsp;&nbsp;**&rarr;** <span style="color: white; background-color: RGBA(194, 193, 194, 60%); border-color: white; border-radius: 3px; padding-left: 6px; padding-right: 6px;">**PostgreSQL database:** </span>
<br>
<span class="tab">Your text goes here.</span>
&nbsp;&nbsp;**&rarr;** <span style="color: white; background-color: RGBA(194, 193, 194, 60%); border-color: white; border-radius: 3px; padding-left: 6px; padding-right: 6px;">**Python webscraper:**</span>
<br>
<span class="tab">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Code file ****webscraper/main.py**** consists of 2 classes: ModelGetter scrapes all car brands and corresponding models using selenium library. It goes through all of the models for each brand by clicking on the dropdown menu. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AdScraper has a function _search_ads_ that uses Beautiful Soup library to scrape latest 100 ads and Zenrows library to avoid anti-bot detection. It stores relevant information for each advertisement on the website to PostgreSQL database.</span>
&nbsp;&nbsp;**&rarr;** <span style="color: white; background-color: RGBA(194, 193, 194, 60%); border-color: white; border-radius: 3px; padding-left: 6px; padding-right: 6px;">**Flask back-end:**</span>
<br>
<span class="tab">We chose to use Flusk as back-end language, for it's lightweight and suitability for our project. It allows easy integration with databases.</span>

# Architecture
<img src="architecture.png" alt="MarineGEO circle logo" style="width:100%; border: 2px solid #1e1e1e; border-radius: 10px; "/>