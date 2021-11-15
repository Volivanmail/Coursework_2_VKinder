import sqlalchemy
from config import DNS
# DNS = 'postgresql://forvk:123vk@localhost:5432/bd_user_vk'

engine = sqlalchemy.create_engine(DNS)
con = engine.connect()

def add_user(user_id):
    try:
        con.execute(f"""
            INSERT INTO vk_user 
            VALUES(DEFAULT, {user_id});
            """)
        con.execute(""" COMMIT; """)
    except:
        pass



def add_user_search(id_user_vk, user_id):
  con.execute(f"""
      INSERT INTO users_from_the_request
      VALUES(DEFAULT, {id_user_vk}, {user_id});
      """)
  con.execute(""" COMMIT; """)

def add_user_favourites(user_id, black_list, id_user_vk):
    con.execute(f"""
        INSERT INTO favourites
        VALUES(DEFAULT, {user_id}, {black_list}, {id_user_vk});
        """)
    con.execute(""" COMMIT; """)

def get_user_search(user_id):
    res = con.execute(f"""
              SELECT vk_user_id FROM users_from_the_request 
              WHERE  {user_id} = user_id;
              """)
    id_user_vk_list = [user[0] for user in res]
    print(id_user_vk_list)
    return id_user_vk_list






