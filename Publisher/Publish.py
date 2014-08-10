# -*- coding: UTF-8 -*-
'''
Created on 27 juil. 2014

@author: ludovicl
'''

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import unicodedata
import markdown2
import os
import io


class Publish(object):

    def __init__(self, website, user, password):
        self.wp = Client(website + "/xmlrpc.php", user, password)
        self.images_link = []


    def post_article(self, content_path, files_path):
        '''
        in : 
            - content_path : content link  
            - files_path : files link in a tuple
        
        out : string with success or error with information 
        '''
        try :
            for f in files_path :
                self._file_updater(str(f))
        except Exception as e :
            return 'Error while uploading images : ' + str(e)

        try :
            if len(content_path) == 1 :
                title, categories, tags, content, = self._content_extract(content_path[0])
            else :
                return 'Error with the content : upload one text file'
        except Exception as e :
            return 'Error while extracting title, categories, tages, content : ' + str(e)

        try :
            html_content = markdown2.markdown(content)
            post = WordPressPost()
            post.title = ' '.join(title)
        except Exception as e :
            return 'Erro while converting in markdown : ' + str(e)

        try :
            # convert unicode in string
            str_content = unicodedata.normalize('NFKD', html_content).encode('ascii', 'ignore')

            # justify paragraphs
            str_content = str_content.replace ('<p>', '<p align=\"justify\">')

            # center images
            str_content = str_content.replace ('<p align=\"justify\"><img', '<p align=\"center\"><img')

            post.content = str_content
            post.post_status = 'publish'

            if isinstance(tags, str):
                tags = tags.split()

            if isinstance(categories, str):
                categories = categories.split()

            post.terms_names = {
                'post_tag': tags,
                'category': categories
                }
        except Exception as e :
            return 'Erro while normalizing html : ' + str(e)

        try :
            erno = self.wp.call(NewPost(post))
        except :
            return "Erro while posting content"

        if erno is not 401 or erno is not 403 or  erno is not 404 :
            ret_value = 'Post successful!'
        else :
            ret_value = 'Error while posting : ' + erno

        return ret_value

    def _file_updater(self, file_path):
        """
        in : string with file link 
        
        out : `dict` with keys `id`, `file` (filename), `url` (public URL), and `type` (MIME-type).
        """
        file_name = os.path.split(file_path)

        if file_name[:3] == 'png':
            data_type = 'image/png'
        else :
            data_type = 'image/jpg'

        # prepare metadata
        data = {
                'name': file_name[1],
                'type': data_type,
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(file_path, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())

        response = self.wp.call(media.UploadFile(data))

        img = {}
        img['url'] = response.get('url')
        img['file'] = response.get('file')

        self.images_link.append(img)

        return response

    def _add_image_to_content(self, image_link, content):
        pass

    def _content_extract(self, p_content):
        """
        in : content as string format with
            -Title
            -Category
            -KeyWords
            -Contents
        out : Title in a list, category in a list, KeyWord in a list, content in a string
        """
        text_content = ''

        with io.open(p_content, 'r', encoding='utf8') as f:

            # Pop call remove "Title :", "Categories :", and "Keywords :"

            title = f.readline().split()
            title.pop(0)
            title.pop(0)

            cat = f.readline().split()
            cat.pop(0)
            cat.pop(0)

            keywords = f.readline().split()
            keywords.pop(0)
            keywords.pop(0)

            for line in f:
                text_content += line

            for d in self.images_link :
                file = d['file']
                url = d['url']

                if text_content.find('(' + file + ')') :
                    text_content = text_content.replace(file, url)

        return title, cat, keywords, text_content


