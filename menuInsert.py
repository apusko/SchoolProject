# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Article
 
engine = create_engine('sqlite:///school.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Menu for UrbanBurger
# category1 = Category(name = u"Электронный журнал", description=u"Онлайн журнал учёта успеваемости учеников, просмотра расписания и связи с классным руководителем.")
# category2 = Category(name = u"Новости", description=u"Просмотр новостной ленты о школьной жизни, а также о ярких моментов проводимых во внеурочное время.")
# category3 = Category(name = u"Наша школа", description=u"Основная информация о школе, преподовательском составе, корпусах, в которых проходят занятия, а также контактные данные и место расположение.")
# category4 = Category(name = u"Прямая линия", description=u"Раздел для просмотра и обращения с вопросами к преподрвательскому составу")
# category5 = Category(name = u"Учебная деятельность", description=u"Здесь хранятся полезные сведения, информация о дополнительных занятиях, кружках и секциях.")
# category6 = Category(name = u"Успеваемость", description=u"Сведения о успеваемости по классам")

# session.add(category1)
# session.add(category2)
# session.add(category3)
# session.add(category4)
# session.add(category5)
# session.add(category6)

# article1 = Article(category_id = 2, name = u"Библиотека", text=u"Библиотека школы № 38 образовалась в 1990 году. В 2006 году библиотека преобразована в библиотечно-информационный центр. Библиотечно-информационный центр функционирует как традиционная библиотека с элементами медиатеки.")
# article2 = Article(category_id = 2, name = u"Столовая", text=u"Рациональное питание - один из основных факторов, ответственных за здоровье человека. Для детей школьного возраста это имеет особое значение в связи с особенностями роста и развития в этот период, а также в связи с интенсивной учебной нагрузкой. Организация рационального питания учащихся является одним из ключевых факторов поддержания их здоровья и эффективности обучения в школе.")

# session.add(article1)
# session.add(article2)

# for i in session.query(Article).all():
# 	i.category_id -= 1
session.commit()
