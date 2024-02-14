from flask import Flask, render_template
from flask import request
from flask import abort
from flask_basicauth import BasicAuth

import pymysql
import os
import json
import math

from collections import defaultdict


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

PAGE_SIZE = 10
MAX_PAGE_SIZE = 50


@app.route("/images/")
# @auth.required
def images():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE)) 
    page_size = min(page_size, MAX_PAGE_SIZE) 
           
    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('MSQLpass'),
                              database="final_project",
                              cursorclass=pymysql.cursors.DictCursor)
    

    with db_conn.cursor() as cursor:
        cursor.execute("""
        SELECT
            ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS pic_nr,
            ei.emotion,
            ds.source,
            ds.url_link,
            height,
            width,
            aspect_ratio,
            image_format,
            color_space,
            file_size_MB,
            pixels
        FROM all_images ai
        JOIN data_sources ds
            ON ai.source_id = ds.id
        JOIN emotions_ids ei
            ON ai.emotion_id = ei.id
        LIMIT %s
        OFFSET %s
        """, (page_size, page * page_size))
            
        images = cursor.fetchall()          
        
        cursor.execute("""
        SELECT COUNT(*) AS total FROM  all_images
        """)
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    
    db_conn.close() 
    
    previous_page_url = f'/images?page={page-1}&page_size={page_size}' if page > 0 else None
    next_page_url = f'/images?page={page+1}&page_size={page_size}' if page < last_page else None
    
    return {
        'images': images,
        'previous_page': previous_page_url,
        'next_page': next_page_url,
        'last_page': f'/images?page={last_page}&page_size={page_size}',
    }     
## ==============================================================================================================
@app.route("/images/<int:image_id>")
def image(image_id):             
    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('MSQLpass'),
                              database="final_project",
                              cursorclass=pymysql.cursors.DictCursor)
    

    with db_conn.cursor() as cursor:
        cursor.execute("""
         WITH numbered_images AS (
            SELECT
                ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS pic_nr,
                ei.emotion,
                ds.source,
                ds.url_link,
                height,
                width,
                aspect_ratio,
                image_format,
                color_space,
                file_size_MB,
                pixels
            FROM all_images ai
            JOIN data_sources ds 
                ON ai.source_id = ds.id
            JOIN emotions_ids ei 
                ON ai.emotion_id = ei.id
        )
        SELECT *
        FROM numbered_images
        WHERE pic_nr = %s
        """, (image_id,))
        
        image = cursor.fetchall()         
    
    db_conn.close() 
    
    if not image:
        abort(404)
    
    return image    

## ===============================================================================================================
@app.route("/images/sources", methods=['GET'])
def images_sources(): 
    source_id = int(request.args.get("source_id")) if request.args.get("source_id") else None
      
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE)) 
    page_size = min(page_size, MAX_PAGE_SIZE) 


    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('MSQLpass'),
                              database="final_project",
                              cursorclass=pymysql.cursors.DictCursor)
    
    
    with db_conn.cursor() as cursor:
        # Base query
        base_query = """
        SELECT 
            ds.source,
            ds.url_link as source_link,
            ei.emotion,
            height,
            width,
            aspect_ratio,
            image_format,
            color_space,
            file_size_MB,
            pixels    
        FROM   
        """
    
        if source_id == 1:
            source_query = """
            images_pixabay pb
            JOIN emotions_ids ei
                ON pb.emotion_id = ei.id
            JOIN data_sources ds
                ON pb.source_id = ds.id
            LIMIT %s
            OFFSET %s
            """      
            
            cursor.execute("""
            SELECT COUNT(*) AS total FROM  images_pixabay pb
            """)
            total = cursor.fetchone()
            last_page = math.ceil(total['total'] / page_size)
            
        elif source_id == 2:
            source_query = """
            images_ddg ddg
            JOIN emotions_ids ei
                ON ddg.emotion_id = ei.id
            JOIN data_sources ds
                ON ddg.source_id = ds.id
            LIMIT %s
            OFFSET %s
            """      
            
            cursor.execute("""
            SELECT COUNT(*) AS total FROM images_ddg
            """)
            total = cursor.fetchone()
            last_page = math.ceil(total['total'] / page_size)            
            
        elif source_id == 3:
            source_query = """
            images_kaggle k
            JOIN emotions_ids ei
                ON k.emotion_id = ei.id
            JOIN data_sources ds
                ON k.source_id = ds.id
            LIMIT %s
            OFFSET %s
            """      
            
            cursor.execute("""
            SELECT COUNT(*) AS total FROM images_kaggle
            """)
            total = cursor.fetchone()
            last_page = math.ceil(total['total'] / page_size)    
            
        elif source_id == 4:
            source_query = """
            images_fer2013 f
            JOIN emotions_ids ei
                ON f.emotion_id = ei.id
            JOIN data_sources ds
                ON f.source_id = ds.id
            LIMIT %s
            OFFSET %s
            """      
            cursor.execute("""
            SELECT COUNT(*) AS total FROM images_fer2013
            """)
            total = cursor.fetchone()
            last_page = math.ceil(total['total'] / page_size) 
        else:
            abort(404)            
            
        full_query = base_query + source_query

        cursor.execute(full_query, (page_size, page*page_size))
        
        img_per_source = cursor.fetchall()
            
    db_conn.close() 
    
    previous_page_url = f'/images/sources?source_id={source_id}&page={page-1}&page_size={page_size}' if page > 0 else None
    next_page_url = f'/images/sources?source_id={source_id}&page={page+1}&page_size={page_size}' if page < last_page else None
    
    return {
        'images': img_per_source,
        'previous_page': previous_page_url,
        'next_page': next_page_url,
        'last_page': f'/images/sources?page={last_page}&page_size={page_size}',
    }   

## Images per EMOTION:=====================================================================================================================
@app.route("/images/emotions", methods=['GET'])
def images_emotions(): 
    emotion = int(request.args.get("emotion")) if request.args.get("emotion") else None
      
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE)) 
    page_size = min(page_size, MAX_PAGE_SIZE) 
    
    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('MSQLpass'),
                              database="final_project",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:   
        base_query = """
        SELECT 
            ds.source,
            ds.url_link,
            ei.emotion,
            height,
            width,
            aspect_ratio,
            image_format,
            color_space,
            file_size_MB,
            pixels
        FROM all_images ai
        JOIN data_sources ds
            ON ai.source_id = ds.id
        JOIN emotions_ids ei
            ON ai.emotion_id = ei.id
        WHERE ei.id = %s
        LIMIT %s 
        OFFSET %s
        """
        condition = None
        
        if isinstance(emotion, int) and emotion >= 0 and emotion <=6:
            condition = emotion
        else:
            abort(404)
    
        cursor.execute(base_query, (condition, page_size, page * page_size))
        img_per_emotion = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM all_images
            WHERE emotion_id = %s
            """, (condition, ))
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
            
    db_conn.close() 
    
    previous_page_url = f'/images/emotions?emotion={emotion}&page={page-1}&page_size={page_size}' if page > 0 else None
    next_page_url = f'/images/emotions?emotion={emotion}&page={page+1}&page_size={page_size}' if page < last_page else None
   
    return {
        'images': img_per_emotion,
        'previous_page': previous_page_url,
        'next_page': next_page_url,
        'last_page': f'/images/emotions?emotion={emotion}&page={last_page}&page_size={page_size}',
    } 

## Images per apect ratio =======================================================================================================
@app.route("/images/aspect_ratio", methods=['GET'])
def images_aspect_ratio(): 
    aspect_ratio = int(request.args.get("aspect_ratio")) if request.args.get("aspect_ratio") else None
    
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE)) 
    page_size = min(page_size, MAX_PAGE_SIZE) 
    
    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('MSQLpass'),
                              database="final_project",
                              cursorclass=pymysql.cursors.DictCursor)
    
    with db_conn.cursor() as cursor:       
        base_query = """
        SELECT 
            ai.id,
            ds.source,
            ds.url_link,
            ei.emotion,
            height,
            width,
            aspect_ratio,
            image_format,
            color_space,
            file_size_MB,
            pixels
        FROM all_images ai
        JOIN data_sources ds
            ON ai.source_id = ds.id
        JOIN emotions_ids ei
            ON ai.emotion_id = ei.id
        WHERE aspect_ratio  {condition}
        LIMIT %s 
        OFFSET %s
        """
        
        if aspect_ratio == 0:
            condition = "< 1"
        elif aspect_ratio == 1:
            condition = "= 1"
        elif aspect_ratio == 2:
            condition = "> 1"    
        else:
            abort(404)
    
        cursor.execute(base_query.format(condition=condition), (page_size, page * page_size))
        
        img_aspect_ratio = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM all_images
            WHERE aspect_ratio {condition}
            """.format(condition=condition))
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)      

        
    db_conn.close() 
    
    previous_page_url = f'/images/aspect_ratio?aspect_ratio={aspect_ratio}&page={page-1}&page_size={page_size}' if page > 0 else None
    next_page_url = f'/images/aspect_ratio?aspect_ratio={aspect_ratio}&page={page+1}&page_size={page_size}' if page < last_page else None
   
    return {
        'images': img_aspect_ratio,
        'previous_page': previous_page_url,
        'next_page': next_page_url,
        'last_page': f'/images/aspect_ratio?aspect_ratio={aspect_ratio}&page={last_page}&page_size={page_size}',
    } 


@app.route("/images/colors", methods=['GET'])
def images_colors(): 
    colors = int(request.args.get("colors")) if request.args.get("colors") else None
    
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE)) 
    page_size = min(page_size, MAX_PAGE_SIZE) 
    
    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('MSQLpass'),
                              database="final_project",
                              cursorclass=pymysql.cursors.DictCursor)
    
    with db_conn.cursor() as cursor:
        base_query = """
        SELECT 
            ai.id,
            ds.source,
            ds.url_link,
            ei.emotion,
            height,
            width,
            aspect_ratio,
            image_format,
            color_space,
            file_size_MB,
            pixels
        FROM all_images ai
        JOIN data_sources ds
            ON ai.source_id = ds.id
        JOIN emotions_ids ei
            ON ai.emotion_id = ei.id
        WHERE color_space = %s
        LIMIT %s 
        OFFSET %s
        """
        
        if colors == 0:
            condition = "Grayscale"
        elif colors == 1:
            condition = "RGB"
        else:
            abort(404)
        
        cursor.execute(base_query, (condition, page_size, page * page_size))
        
        img_colors = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM all_images
            WHERE color_space = %s
            """, condition, )
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)  
        
        
    db_conn.close() 
    
    previous_page_url = f'/images/colors?colors={colors}&page={page-1}&page_size={page_size}' if page > 0 else None
    next_page_url = f'/images/colors?colors={colors}&page={page+1}&page_size={page_size}' if page < last_page else None
   
    return {
        'images': img_colors,
        'previous_page': previous_page_url,
        'next_page': next_page_url,
        'last_page': f'/images/colors?colors={colors}&page={last_page}&page_size={page_size}',
    }


# =================================================================================
@app.route("/images/emotions/faces", methods=['GET'])
def faces():      
    face = request.args.get("face") 
        
    db_conn = pymysql.connect(host="localhost", 
                              user="root", 
                              password=os.getenv('MSQLpass'),
                              database="final_project",
                              cursorclass=pymysql.cursors.DictCursor)
    
    try:
        face = int(face)
        
        if face in [0, 1, 2, 3, 4, 5, 7]:       
            with db_conn.cursor() as cursor:
                cursor.execute("""
                SELECT 
                    id,
                    ei.emotion,
                    action_unit,
                    fs.description,
                    facial_muscle,
                    example
                FROM (
                    SELECT * 
                    FROM emotions_ids 
                    WHERE id = %s) as ei
                JOIN facs_emotions_units feu
                    ON ei.id = feu.emotion
                JOIN facs_single_units fs
                    ON feu.action_units = fs.action_unit;
                """, (face,))

                faces = cursor.fetchall()
        else:
            abort(404)
    
    except ValueError:
        abort(400)  # Bad Request: The provided value for 'face' is not a valid integer
    
    finally:
        db_conn.close()  # Ensure the database connection is always closed
    
    return faces
