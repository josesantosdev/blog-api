from flask import Blueprint, request, Response, json, g 
from flask_jwt_extended import jwt_required
from app.models.blog_post_model import BlogPost, BlogPostSchema

class BlogPostController:

    blog_post_controller = Blueprint('blog_post_controller', import_name=__name__)

    @blog_post_controller.route('/blogpost', methods=['POST'])
    @jwt_required
    def create_blog_post():
        request_data = request.get_json()
        request_data['owner_id'] = g.user.get('id')
        try:
            data = blog_post_schema.load(request_data)
        except Exception:
            return custom_response({'error': 'payload request error'}, 500)
        
        blog_post = BlogPost(data)
        blog_post.save

        serealized_blog_post = blog_post_schema.dump(blog_post)
        return custom_response(serealized_blog_post, 201)


    @blog_post_controller.route('/blogpost', methods=['GET'])
    @jwt_required()
    def get_all_blog_posts():
        
        
        all_blog_posts = BlogPost.get_all_blogposts()
        
        if not all_blog_posts:
            return custom_response({'message': 'make your first post'},200)

        serealized_blog_posts = blog_posts_schema.dump(all_blog_posts)
        
        return custom_response(serealized_blog_posts, 200)

    
    @blog_post_controller.route('/blogpost/<id>', methods=['GET'])
    @jwt_required()
    def get_one_blog_posts(id):
        blog_post = BlogPost.get_one_blogpost(id)
        
        if not blog_post:
            return custom_response({'error':'blog post not find'}, 404)

        serealized_blog_post = blog_post_schema(blog_post)

        return custom_response(serealized_blog_post, 200)
    

    @blog_post_controller.route('/blogpost/<id>', methods=['PUT'])
    @jwt_required()
    def update_blog_posts(id):
        request_data = request.get_json()
        blog_post = BlogPost.get_one_blogpost(id)

        try:
            data = blog_post_schema(request_data)
        except Exception:
            return custom_response({'error': 'payload request error'}, 500)


        if not blog_post:
            return custom_response({'error':'blog post not find'}, 404)
        
        if data.get('owner_id') != g.user.get('id'):
            return custom_response({'error': 'permission danied'}, 400)

        blog_post.update(data)

        serealized_blog_post = blog_post_schema(blog_post)

        return custom_response(serealized_blog_post, 200)



    @blog_post_controller.route('/blogpost/<id>', methods=['DELETE'])
    @jwt_required()
    def delete_blog_posts(id):
        blog_post = BlogPost.get_one_blogpost(id)

        if not blog_post:
            return custom_response({'error':'blog post not find'}, 404)

        serealized_blog_post = blog_post_schema.dump(blog_post)

        if serealized_blog_post.get('owner_id') != g.user.get(id):
            return custom_response({'error': 'permission danied'}, 400)

        blog_post.delete()

        return custom_response({'message': 'deleted'}, 200)



    
blog_post_schema = BlogPostSchema()
blog_posts_schema = BlogPostSchema(many=True)
    
def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )