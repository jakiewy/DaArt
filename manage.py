# -*- encoding=UTF-8 -*-

from dada import app, db
from flask_script import Manager
from sqlalchemy import or_, and_
from dada.models import User, Image, Comment
import random

manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('游客' + str(i), 'a' + str(i)))

        for j in range(0, 10):  # 每人发十张图
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('这是一条评论' + str(k), 1 + 10 * i + j, i + 1))
    db.session.commit()

    # '''
    # 更新
    for i in range(0, 100, 3):
        # 通过update函数
        User.query.filter_by(id=i).update({'username': '33游客新' + str(i)})

    # User.query.filter(User.username.endswith('0')).update({'username': '00新' + User.username}, synchronize_session=False)
    # filter_by多个参数是and
    User.query.filter_by(id=4, password='a4').update({'username': '44游客新' + str(i)})
    User.query.filter_by(id=5, password='a4').update({'username': '55游客新' + str(i)})

    for i in range(7, 100, 10):
        # 通过设置属性
        u = User.query.get(i)
        u.username = '77' + str(i * i)
    db.session.commit()

    # 删除
    for i in range(50, 100, 2):
        Comment.query.filter_by(id=i + 1).delete()
    for i in range(51, 100, 2):
        comment = Comment.query.get(i + 1)
        db.session.delete(comment)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
