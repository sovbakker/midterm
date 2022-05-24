# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import urllib.request

with st.echo(code_location='below'):
    @st.cache
    def get_data_agestandart():
        return pd.read_csv("https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/Agestandardized_suicide_rates.csv")

    agestandart=get_data_agestandart()

    @st.cache
    def get_data_crude():
        return pd.read_csv("https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/Crude_suicide_rates.csv")

    crude=get_data_crude()

    @st.cache
    def get_data_facilities():
        return pd.read_csv("https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/Facilities.csv")

    facilities=get_data_facilities()

    @st.cache
    def get_data_HR():
        return pd.read_csv("https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/Human_Resources.csv")

    HR=get_data_HR()

    @st.cache(allow_output_mutation=True)
    def get_data_masterdata():
        return pd.read_csv("https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/master.csv")

    masterdata=get_data_masterdata()

    @st.cache(allow_output_mutation=True)
    def get_data_ISO():
        return pd.read_csv("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")

    ISO = get_data_ISO()

    @st.cache(allow_output_mutation=True)
    def get_data_GI():
        return pd.read_csv("https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/Gender%20Inequality%20Index.csv")

    GI=get_data_GI()

    @st.cache()
    def get_data_GDP():
        return pd.read_csv("https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/GDP.csv")

    GDP=get_data_GDP()

    #agestandart

    #crude

    #facilities

    #HR

    #masterdata

    #ISO

    #GI

    menu=["Yearly statistics in Europe", "World early statistics", "Facilities and Human Resources", "Gender inequality", "Age and generations"]

    st.sidebar.markdown('''
    # Sections
    - [Intro](#suicides)
    - [Yearly statistics in Europe](#yearly-statistics-in-europe)
    - [World early statistics](#world-early-statistics)
    - [Facilities and Human Resources](#facilities-and-human-resources)
    - [Gender inequality](#gender-inequality)
    - [Age and generations](#age-and-generations)
    - [Interaction](#interaction)
    - [Outro](#results)
    ''', unsafe_allow_html=True)

    ISO["name"]=ISO["name"].replace("Korea, Republic of","Republic of Korea")

    GI["Country"]=GI["Country"].replace("United States", "United States of America")

    masterdata["country"]=masterdata['country'].replace("United States", "United States of America")

    masterdata_for_teens=masterdata[masterdata["age"]=="15-24 years"]

    masterdata_for_teens=masterdata_for_teens.groupby(["year", "country"]).sum()

    masterdata_for_teens=masterdata_for_teens.reset_index().sort_values("year", ascending=True)

    masterdata_for_teens['share on 100k']=masterdata_for_teens['suicides_no']/masterdata_for_teens['population']*100000

    masterdata_for_teens=masterdata_for_teens.merge(ISO, left_on="country", right_on='name', how="inner").drop(columns="name")

    masterdata_for_teens=masterdata_for_teens.sort_values("year", ascending=True)

    agregated_masterdata=masterdata.groupby(["year", "country"]).sum('suicides_no')

    agregated_masterdata['share on 100k']=agregated_masterdata['suicides_no']/agregated_masterdata['population']*100000

    agregated_masterdata = agregated_masterdata.reset_index()

    agregated_masterdata=agregated_masterdata.merge(ISO, left_on="country", right_on='name', how="inner").drop(columns="name")

    agregated_masterdata.sort_values('year', inplace=True)

    agregated_masterdata=agregated_masterdata[agregated_masterdata['year']!=2016]

    #agregated_masterdata

    agregated_masterdata_europe=agregated_masterdata[agregated_masterdata['region']=='Europe']

    eu_year_share=agregated_masterdata_europe.groupby('year').mean('share on 100k').reset_index()

    #eu_year_share

    agregated_masterdata_without_europe=agregated_masterdata[agregated_masterdata['region']!='Europe']

    noneu_year_share=agregated_masterdata_without_europe.groupby('year').mean('share on 100k').reset_index()

    #noneu_year_share

    agestandart_2_0=agestandart.drop(columns=['2015', "2010", "2000"]).merge(ISO, left_on='Country', right_on='name', how='inner')\
        .drop(columns='name')

    agestandart_2_0_bothsexes = agestandart_2_0[agestandart_2_0["Sex"].str.contains("Both")].drop(columns="Sex").reset_index(drop=True)

    agestandart_2_0_bothsexes_with_facilities=agestandart_2_0_bothsexes.merge(facilities, on="Country", how='inner')

    agestandart_2_0_bothsexes_with_facilities=agestandart_2_0_bothsexes_with_facilities.rename(
        columns={"Mental _hospitals":"Mental hospitals (inpatient)", "health_units":"Health Units", "outpatient _facilities":"Outpatient facilities",
                 "day _treatment":"Day treatment", "residential_facilities":"Residential facilities", '2016':'Suicide Rate'})

    #agestandart_2_0_bothsexes_with_facilities

    #agestandart_2_0_bothsexes

    agestandart_2_0_bothsexes_with_HR=agestandart_2_0_bothsexes.merge(HR, on="Country", how='inner').rename(
        columns={"Social_workers":"Social workers", "2016":"Suicide rate"})

    agestandart_2_0_bothsexes_with_HR_eu_only=agestandart_2_0_bothsexes_with_HR[agestandart_2_0_bothsexes_with_HR['region']=='Europe']

    st.title("Suicides")
    st.header("Или, говоря по-русски, суициды! :hole::walking:")

    st.write("""
    Этот проект не создавался для того, чтобы донести какую-то мысль или убедить читателя в чем-либо. Я просто нашел 
    несколько интересных датасетов, связанных с темой самоубийств и попробую воспользоваться ими, чтобы продемонстрировать 
    интересные закономерности, некоторые из которых могут казаться контринтуитивными. Ну и, естественно, будет много разных графиков!
    """)

    st.header("Yearly statistics in Europe")

    st.write("""
    Для начала посмотрите вот на эту карту. Двигайте ползунок снизу, чтобы смотреть статистику за разные годы.
    """)



    bettersmallmak=px.choropleth(agregated_masterdata, locations="alpha-3", title="Кол-во суицидов на 100'000 человек в год",
                         hover_name="country", color="share on 100k",
                         animation_frame="year", range_color=(0,45),
                         projection="natural earth", scope='europe', color_continuous_scale='YlOrRd')

    smallmak=px.scatter_geo(masterdata_for_teens, locations="alpha-3", title="Кол-во суицидов на 100'000 человек в год среди подростков",
                         hover_name="country", size="share on 100k",
                         animation_frame="year",
                         projection="natural earth", scope='europe')



    st.plotly_chart(bettersmallmak)

    st.plotly_chart(smallmak)

    eu_mean_chart=alt.Chart(eu_year_share, title="Кол-во суицидов на 100'000 человек в странах Европы").mark_bar().encode(
        x=alt.X("year", scale=alt.Scale(domain=[1985, 2015])),
        y=alt.Y('share on 100k', scale=alt.Scale(domain=[6, 22]))
    )

    st.altair_chart(eu_mean_chart, use_container_width=True)

    st.write("""
    Можно заметить, что пиковые значения приходятся на конец девяностых. Причем это происходит не только в странах Восточной 
    Европы, горюющих о распаде СССР, но и странах Западной Европы, например, во Франции. Но в XXI веке частота суцидов резко снижается с небольшим 
    скачком в 2008 году. Теперь давайте посмотрим на это в контексте всего мира.
    """)

    st.header("World early statistics")

    betterbigmapk=px.choropleth(agregated_masterdata, locations="alpha-3", title="Доля самоубиств на 100'000 человек",
                         hover_name="country", color="share on 100k",
                         animation_frame="year", range_color=(0,45),
                         projection="natural earth", color_continuous_scale='YlOrRd')

    bigmapk=px.scatter_geo(masterdata_for_teens, locations="alpha-3", color="region", title="Доля самоубиств на 100'000 человек среди подростков",
                         hover_name="country", size='share on 100k',
                         animation_frame="year",
                         projection="natural earth")

    st.plotly_chart(betterbigmapk)

    st.plotly_chart(bigmapk)

    noneu_mean_chart=alt.Chart(noneu_year_share, title="Доля самоубиств на 100'000 человек в странах, не являющихся европейскими").\
        mark_bar().encode(
        x=alt.X("year", scale=alt.Scale(domain=[1985, 2015])),
        y=alt.Y('share on 100k', scale=alt.Scale(domain=[6, 22]))
    )

    st.altair_chart(noneu_mean_chart, use_container_width=True)

    st.write("""
    К сожалению, за данный период нет точных данных про многие страны, но довольно хорошо заметно, что кроме Кубы, переживавшей в 
    1990-х года тяжелейший кризис, доля самоубиств в большинстве неевропейских почти не изменялась. Более того, я специально 
    установил одинковый масштаб графиков, чтобы вы могли увидеть на сколько в Европе в среднем больше самоубийств на душу населения 
    чем во всем остальном мире. Распространенное представление о суициде состоит в том, что если вы бедность приводит к депрессивному образу жизни и сопутсвующим социальным проблемам, 
    еще более ухудшающими внутрненнее состояние люди.
    Некоторые самоубийства также происходят из-за финансовых потерь (см 2008 год), проблем в отношениях или буллинга.
    Однако наши данные данные свидетельствуют о том, что в странах развитого мира больше случаев самоубийств, чем в развивающихся и слаборазвитых странах.
    """)

    st.write("""
    Один экономист, которого почему-то все цитируют, но не называют по имени, обяснил эту закономерность следующим образом: 
    «Бедные люди в развивающихся странах выживают и часто находят удовольствие в своей тяжелой жизни. 
    В беднейших странах мало самоубийств. У кого есть время на самоубийство? Ты слишком занят выживанием». У этой закономерности нет называния, поэтому давайте назовем ее 'Парадокс хорошей жизни' для удобства.
    Страны Европы гораздо богаче большинства других стран, поэтому тут можно было бы сказать про то, что развитие экономики нарушает стандартные стимулы в жизнях людей, 
    что подрывает их психологическое здоровье и приводит к самоубийствам. Но тогда сразу происходит противоречие с диномикой изменения колличества самоубиств 
    в самой Европе, когда активное развитие экономики в XXI веке происхдило одновременно со снижением числа самоубиств, поэтому заявлять подобное наверняка не стоит.
    """)

    st.header("Facilities and Human Resources")

    st.write("""
    Можно предположить, что правительства европейских стран в девяностые спохватились и начали активно развивать психическую 
    медицину и связанную с ней инфраструктуру, что привело к снижению колличества суицидов. Мы можем очень просто проверить 
    эффективно ли подобное лечение в борьбе с суицидами. Ниже вы можете посмотреть на данные карты ковариаций числа различных
    медицинских учреждений на 100'000 человек населения и суицидальности в Европе. Я использую именно данные по европе, чтобы
    избежать проблем с установкой причино-следственных связей.
    """)

    agestandart_2_0_bothsexes_with_facilities_europe_only=agestandart_2_0_bothsexes_with_facilities[
        agestandart_2_0_bothsexes_with_facilities['region']=='Europe']

    GDP16=GDP.drop(columns=["1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2017","2018","2019"]).rename(columns={"2016":"GDP per capita"})

    agestandart_2_0_bothsexes_with_facilities_europe_only=agestandart_2_0_bothsexes_with_facilities_europe_only.merge(GDP16, left_on="alpha-3", right_on="Country Code", how="left")

    facility_options=["Mental hospitals (inpatient)", "Health Units", "Outpatient facilities",
                 "Day treatment", "Residential facilities"]

    facility=st.selectbox("Выберите любой вид учреждения", facility_options)

    heat=alt.Chart(agestandart_2_0_bothsexes_with_facilities_europe_only).mark_circle().encode(
        x=facility,
        y="Suicide Rate:Q",
        tooltip=['Country', 'Suicide Rate'],
        size="GDP per capita:Q"
    )

    heat = heat + heat.transform_regression(facility, 'Suicide Rate').mark_line()

    st.altair_chart(heat, use_container_width=True)

    st.write("""
    Как видно повышения кол-ва различных видов подобных учреждений почти никак не меняет ситуацию. Теперь давайте проверим 
    есть ли какой-то эффект на число суицидов от человеческих ресурсов в психологии и медицине.
    """)

    HR_options=["Psychiatrists", "Nurses", "Social workers", "Psychologists"]

    HR1=st.selectbox("Выберите профессию", HR_options)

    #agestandart_2_0_bothsexes_with_HR_eu_only

    agestandart_2_0_bothsexes_with_HR_eu_only=agestandart_2_0_bothsexes_with_HR_eu_only.merge(GDP16, left_on="alpha-3", right_on="Country Code", how="left")

    heat=alt.Chart(agestandart_2_0_bothsexes_with_HR_eu_only).mark_circle().encode(
        x=HR1,
        y="Suicide rate:Q",
        tooltip=['Country', 'Suicide rate'],
        size="GDP per capita:Q"
    )

    heat = heat + heat.transform_regression(HR1, 'Suicide rate').mark_line()

    st.altair_chart(heat, use_container_width=True)

    #agestandart_2_0_bothsexes_with_HR_eu_only

    f1f1=np.array(agestandart_2_0_bothsexes_with_HR_eu_only[agestandart_2_0_bothsexes_with_HR['Nurses'].notna()]['Suicide rate'])
    f2f2=np.array(agestandart_2_0_bothsexes_with_HR_eu_only['Nurses'].dropna())

    corcoeffornurses=np.corrcoef(f1f1, f2f2)



    st.write("""
    Из всех проффесий только доля медсестер показывает значительную корреляцию, а именно 0.5648, как видно на картинке ниже.
    """)

    st.write(corcoeffornurses)

    st.write("""
    Но коэффициент положительный, что означает, что в европейских обществах, где много медсестер, много и самоубиств.
    Но это опять же объясняется просто банальным уровнем развития стран, то есть страны более экономически развитые имеют 
    больше число людей с высшим образованием, в особенности в таких сложных сферах как медицина, но одновременно экономическое развитее приводит к 'Парадоксу хорошей жизни'.
    """)

    st.write("""
    Итак, на данном этапе мы лишь понимаем, что ничего не понимаем, потому что выводы мы имеем пока только такие: 1) создание 
    инфраструктуры по лечению психических и психологических не имеет явного эффекта в борьбе с суицидами; 
    2) вероятность, что житель бедной страны убьет себя гораздо меньше (в среднем в три раза) чем вероятность, что себя убьет житель богатой страны, 
    что особенно странно, учитывая, что житель бедной страны может только мечтать о проблемах жителя богатой страны.
    """)

    st.header("Gender inequality")

    st.write("""
    Теперь я хочу разобрать аргумент известного проффессора психологии Джордана Питерсона, который он использовал в споре о гендерном неравенстве во время интервью. 
    Пожалуйста, посмотрите короткий отрывок ниже.
    """)

    @st.cache(allow_output_mutation=True)
    def vido():
        return urllib.request.urlretrieve("https://github.com/SovBakoid/suicides/raw/main/suicide_data/Jorgi.mp4", "Jordan Peterson Completely Destroys Feminist Narrative.mp4")

    video1, something_else=vido()

    st.video(video1)

    st.write("""
    Правда ли, что доля самоубийств мужчин в общем числе самоубиств является хорошим индикатором 
    отсутствия гендерного неравенства? 
    """)

    st.write("""
    Для начала посмотрите просто на уровень суициодов в разных странах среди женщин.
    """)

    agestandart_male=agestandart[agestandart["Sex"]==" Male"].reset_index(drop=True)

    agestandart_female=agestandart[agestandart['Sex']==" Female"].reset_index(drop=True)

    agestandart_female_sorted = agestandart_female.sort_values(by='2016', ascending=False).rename(columns={"2016":"Suicide Rate"})

    agestandart_female_sorted=agestandart_female_sorted.merge(ISO, left_on="Country", right_on="name", how="left").fillna("no data")

    beautiful_bars = px.bar(agestandart_female_sorted, x='Country', y="Suicide Rate", title="Suicide Rate Among Women In Diffrent Countries", width=100)

    st.plotly_chart(beautiful_bars, use_container_width=True)

    st.write("""
    На графике выше не так хорошо видны отдельные страны, но можно проследить закономерность,
    что наиболее высокий уровень самоубийств среди женщин в странах Центральной Африки, а 
    самый низкий на удивление в мусульманских странах Персидского залива, таких как ОАЭ, Катар, 
    Оман. Страны Европы же находятся примерно во второй четверти данного графика. 
    Для удобства ниже я построил еще один только для стран Европы и Персидского залива.
    """)

    agestandart_female_sorted_eu_n_persian=agestandart_female_sorted[(agestandart_female_sorted["sub-region"]=="Western Asia") | (agestandart_female_sorted["sub-region"]=="Eastern Europe") | (agestandart_female_sorted["sub-region"]=="Northern Europe") | (agestandart_female_sorted["sub-region"]=="Western Europe")]

    agestandart_female_sorted_eu_n_persian["region"]=agestandart_female_sorted_eu_n_persian["region"].replace({"Asia":"Near East"})

    beautiful_bars2 = px.bar(agestandart_female_sorted_eu_n_persian, x='Country', y="Suicide Rate", title="Suicide Rate Among Women In Diffrent Countries", color="region")

    st.plotly_chart(beautiful_bars2, use_container_width=True)

    st.write("""
    Как видно, в странах Западной Азии Suicide Rate гораздо ниже и тут не работает даже парадокс Хорошей Жизни, так как, например, Катар входит в топ-3 стран по ВВП на душу населения и имеет Suicide Rate ниже чем все страны Европы. 
    Если не разбираться дальше, то можно сделать вывод, что культуры, угнетающие женщин, способны богатеть без повышеня уровня женской суицидальнсти.
    Но если копнуть чуть глубже, то мы видим вот такую закономерность. 
    """)

    agestandart_mf_proportion=agestandart_male['2016']/agestandart_female['2016']

    agestandart_mf_proportion_df=pd.DataFrame({'Country':agestandart_male["Country"], "male/female suicides proportion": agestandart_mf_proportion})

    #agestandart_mf_proportion_df

    GI["Country"]=GI["Country"].str.strip()

    agestandart_mf_proportion_df_GI=agestandart_mf_proportion_df.merge(GI.drop(columns=["1995","2000", "2005", "2010", "2011", "2012", "2013", "2014", "2015", "2017"]).rename(
        columns={"2016":"Gender Inequality Index","HDI Rank":"Human Development Index Rank"}),on='Country', how="inner")

    agestandart_mf_proportion_df_GI["Human Development Index Rank"]=pd.to_numeric(agestandart_mf_proportion_df_GI["Human Development Index Rank"])

    #agestandart_mf_proportion_df_GI

    sns.set_theme(style="ticks")

    fig1337, ax = plt.subplots()

    fig1337=sns.jointplot(x="Gender Inequality Index", y="male/female suicides proportion", data=agestandart_mf_proportion_df_GI,
                            kind="reg", truncate=False,
                            xlim=(0,1), ylim=(0, 8),
                            color="m", height=7)

    st.pyplot(fig1337)

    st.write("""
    То есть все-таки при повышении уровня гендерного неравенства пропорция самоубиств, совершенных мужчинами и женщинами, выравнивается,
    что означает, что женщины совершают большее относительное число самоубийств в странах, где их угнетают. Кстати, по дополнительным 
    элементам графика справа видно, что в среднем (по странам, то есть без оценки по колличеству населения) на каждое самоубийство, 
    совершенное женщиной, приходится примерно три самоубиства, совершенных мужчиной.
    """)

    st.write("""
    Теперь рассмотрим соответствие половой пропорции суицидов и индекс развития человеческого потенциала, который определяется 
    по уровню жизни, грамотности, образованности и долголетию.
    """)

    fig1338, ax2 = plt.subplots()

    fig1338=sns.jointplot(x="Human Development Index Rank", y="male/female suicides proportion", data=agestandart_mf_proportion_df_GI,
                      kind="kde", truncate=False, xlim=(0,200), ylim=(0, 8),
                      color="m",  cmap="YlGnBu", shade=False)

    st.pyplot(fig1338)

    st.write("""
    Как видно, общий тренд на этом графике довольно схож с предыдущим, что довольно понятно, так как HDI и GII сильно скоррелированы.
    Важно заметить, что в странах, входящих в топ-25 по HDI, наблюдается снижение пропорционального разрыва. Возможным 
    объяснением этого заключается в том, что даже в самых эгалитарных страннах все-равно сохраняется определенный уровень неравенства,
    из-за чего только в случае, если в общем население особенно богато, то менее властные слои населения тоже испытывают парадокс хорошей жизни.
    """)

    st.write("""
    После всего высшесказанного, правда ли, что доля самоубийств мужчин в общем числе самоубиств является хорошим индикатором 
    отсутствия гендерного неравенства? Я считаю, что нет. Во-первых, мы видим эффект, что в патриархальных обществах (на примере 
    стран Персидского залива) низкий уровень суицида среди женщин. Во-вторых, эта метрика очень плохо работает абстрактно от общего уровня жизни,
    так как он сильнее всего влияет на частоту суицидов в различных общнастях.
    """)

    st.subheader("Age and generations")

    st.write("""
    Теперь давайте посмотрим на поло-возрастную мировую статистику. По умолчанию установлены все страны в мире, но вы также можете
    выбрать конкретную интересующую вас страну.
    """)

    crude=crude.rename(columns={' 80_above': "80+", ' 70to79': "70-79", ' 60to69 ': "60-69", ' 50to59 ':"50-59",
           ' 40to49': "40-49", ' 30to39':"30-39", ' 20to29':"20-29", ' 10to19':"10-19"})

    Countries232=pd.unique(crude["Country"]).tolist()

    Countries232=["All countries"] + Countries232

    crude1=crude.melt(id_vars=["Country", "Sex"]).rename(columns={"variable":"Age", "value":"Suicide Rate"})

    crude1=crude1.sort_values(["Country", "Sex", "Age"], ascending=[True, False, True]).reset_index(drop=True)

    crude1["Suicide Rate"]=crude1["Suicide Rate"].astype(float)

    crude2=crude1[crude1["Sex"]!=" Both sexes"]

    picker4 = st.selectbox("Выберите страну", Countries232)

    yay, ax3 = plt.subplots()

    if picker4 == "All countries":
        sns.stripplot(x="Age", y="Suicide Rate", data=crude2, hue="Sex", dodge=True, ax=ax3)
    else:
        sns.stripplot(x="Age", y="Suicide Rate", data=crude2[crude2["Country"]==picker4], hue="Sex", dodge=True, ax=ax3)

    st.pyplot(yay)

    st.write("""
    Тут явно видно, что Suicide Rate в 2016 году был наибольшим у пожилого населения. Теперь проверим является ли это особенностью поколений или возраста.
    Для этого я возьму все доступные данные с 1985 года и сгруппирую их по поколениям.
    """)

    masterdata111=masterdata.groupby(["country", "generation"]).mean().drop(columns="year").reset_index()

    custom_dict = {"G.I. Generation":0, "Silent":1, "Boomers":2, "Generation X":3, "Millenials":4, "Generation Z":5}

    masterdata111.sort_values("generation", inplace=True, key=lambda x: x.map(custom_dict))

    yay2, ax4 = plt.subplots()

    sns.stripplot(x="generation", y="suicides/100k pop", data=masterdata111, dodge=True, ax=ax4, palette="YlGnBu")

    yay2.set_size_inches(11.7, 8.27)

    st.pyplot(yay2, use_container_width=True)

    st.write("""
    Как видно, число суициодов снижается постепенно с каждым поколением. Так как мы обладаем лишь данными за 1985-2016 годы, а не за все время существования каждого их поколений, 
    а также знаем, что динамики по изменению suicide rate за имеющийся период не было, мы можем сделать вывод, что это
    именно возраст, а не принадлежность к определенному поколению приводит к изменению частоты суицидов.
    """)

    st.header("Interaction")

    st.write("""
    А теперь небольшой интерактив.
    """)

    st.write("""Расскажите о себе""")

    col1, col3, col2=st.columns([3,2,3])

    polpol=["Male", "Female"]

    Countries282=pd.unique(crude["Country"]).tolist()

    canatary=col1.selectbox("В какой стране вы живете?", Countries282)

    datatata=col2.date_input("Пожалуйста, ведите вашу дату рождения",  min_value=pd.to_datetime('1900-01-01', format='%Y-%m-%d'),
                             max_value=pd.to_datetime('today', format='%Y-%m-%d'))

    sexax=col3.radio("Пожалуйста, укажите ваш пол", polpol)

    datatata=datatata.year

    agenow=2022-datatata

    if agenow<20:
        agenow="10-19"
    elif agenow<30:
        agenow="20-29"
    elif agenow<40:
        agenow="30-39"
    elif agenow<50:
        agenow="40-49"
    elif agenow<60:
        agenow="50-59"
    elif agenow<70:
        agenow="60-69"
    elif agenow<80:
        agenow="70-79"
    elif agenow>80:
        agenow="80+"

    resultforyou=crude2[(crude2["Country"]==canatary) & (crude2["Age"]==agenow) & (crude2["Sex"].str.strip()==sexax)]

    resultforyou=resultforyou.reset_index(drop=True)["Suicide Rate"][0]

    if st.button("Submit"):
        st.write(f'Люди вашего пола и возраста в вашей стране совершают суицид *{resultforyou}* раз на сто тысяч человек в год. Это безумно мало. Шанс, что такой же человек как вы совершит суицид в этом году равен *{resultforyou/100000}*, что по факту равно нулю! И это првильно, потому что в суициде нет ничего хорошего.')

    photsas=st.camera_input("Теперь дайте мне на вас посмотреть")

    if photsas:
        if sexax=="Male":
            st.success("Вы очень красивый! Надеюсь такой красавчик никогда себя не убьет :heartbeat:")
        elif sexax=="Female":
            st.success("Вы очень красивая! Надеюсь такая красавица никогда себя не убьет :heartbeat:")

    st.header("Results")

    st.write("""
    В результате нашего исследования, мы пришли к выводу, что ключевыми факторами, влиящими на Sucide Rate, являются: 
    уровень жизни, культура и возраст обозреваемой группы. 
    """)

    F1=st.checkbox("Я считаю, что в шутках про суицид нет ничего плохого.")

    @st.cache()
    def imagge2():
        response = requests.get('https://raw.githubusercontent.com/SovBakoid/suicides/main/suicide_data/samurai2.jpg')
        return Image.open(BytesIO(response.content))

    image2=imagge2()

    if F1:
        st.info("Вы точно так считаете?")
        if st.checkbox("Я точно считаю, что в шутках про суицид нет ничего плохого."):
            st.info("А если вы все-таки оскорбитесь за подобную шутку, не относящуюся к контексту учебы, мне придет за это дисциплинарка?")
            if st.checkbox("Обещаю, что нет!"):
                st.image(image2, caption='ИЗВИНИТЕ')

    st.subheader("Использованные источники")

    st.write("""
    https://www.kaggle.com/datasets/russellyates88/suicide-rates-overview-1985-to-2016\n
    https://www.kaggle.com/datasets/twinkle0705/mental-health-and-suicide-rates\n
    https://www.youtube.com/watch?v=yZYQpge1W5s&t=3482s\n
    https://www.kaggle.com/datasets/tjysdsg/gender-inequality-index\n
    https://www.kaggle.com/datasets/andradaolteanu/country-mapping-iso-continent-region\n
    https://www.kaggle.com/datasets/nitishabharathi/gdp-per-capita-all-countries\n
    https://vt.tiktok.com/ZSdHjJ71B/?k=1
    """)