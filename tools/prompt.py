
def create_promt_embeding(row):
    numbers_per = ['اول','دوم','سوم','چهارم','پنجم']

    movie_tilte =  'فیلم : {fa_name} ({name})'.format(name = row['name'] ,fa_name = row['name_fa']) if str(row['name_fa']) != 'nan' else 'فیلم :{name} '.format(name = row['name'] )
    movie_actors = 'بازیگران : {actors}'.format(actors=' , '.join(eval(row['actors']))) 
    movie_genres = 'ژانرهای فیلم : {genres}'.format(genres=' , '.join(eval(row['genres'])))
    movie_imbd_score = '{imdb_score} : imdb امتیاز'.format(imdb_score = row['imdb_score'])if str(row['imdb_score']) != 'nan' else None
    movie_relase = 'سال ساخت : {release}'.format(release = row['release'])
    movie_countries = 'کشور های سازنده : {countries}'.format(countries = ' , '.join(eval(row['countries'])))
    movie_directors = 'کارگردان : {directors}'.format(directors = ' , '.join(eval(row['directors'])))
    movie_authors = 'نویسنده : {authors}'.format(authors = ' , '.join(eval(row['authors'])))
    movie_desc =  [item for item in [row['summary_digi'],row['summary_kio'],row['summary_tiny'],row['summary_uptv'],row['story']] if str(item) != 'nan']
    movie_desc = "خلاصه فیلم : {description}".format(description = movie_desc[0]) if len(movie_desc) == 1 else '\n'.join([f"خلاصه {numbers_per[i]} فیلم : {description}" for i, description in enumerate(movie_desc)])  
    movie_prompt =  '\n\n'.join([movie_tilte,movie_actors,movie_genres,movie_relase,movie_countries,movie_directors,movie_authors] +  ([movie_imbd_score] if movie_imbd_score else []) + [movie_desc] )
    return movie_prompt


def create_promt_querry(querry):
    return f"""فیلمی را پیدا کنید که این ویژگی ها را برآورده کند : 
{querry}
    """
    
def createe_promt_geneartive(row_ids,df,querry):
    row_ids = [int(row_id) for row_id in row_ids]
    select_row = df[df['idf'].isin(row_ids)]
    response = []
    for index, row in select_row.iterrows():
        response.append(create_promt_embeding(row)) 
    response =  "نتیجه جستوجو : {response}".format(response = response[0]) if len(response) == 1 else '\n'.join([f"جستوجو: {i+1} نتیجه : {respons}" for i, respons in enumerate(response)])
    return f""" 
کاربر به دنبال فیلم با مشخصات زیر است:
{querry}
--------
نتایج زیر بیش ترین شباهت را با درخواست کاربر داشته است:
{response}
----------
به عنوان یک دستیار کاربر ، متن مناسب از نتایج حاصل جست جو با توجه به مشخصات فیلم درخواستی کاربر بنویسید.
    """
    

