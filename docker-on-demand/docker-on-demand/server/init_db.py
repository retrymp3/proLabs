from database import db, Users, Challenges, SolvedChallenges, Deployment

def dummyData() :
        user1 = Users(id=0, user_id=1000, username='John Doe',password='1234', email='johndoe@doeing.in')
        user2 = Users(id=1, user_id=1001, username='Alice',password='12345', email='alice@wonderland.in')

        chall1 = Challenges(chall_id=0, chall_name='csrf_chall', chall_point=120)
        chall2 = Challenges(chall_id=1, chall_name='xss_chall', chall_point=100)
        chall3 = Challenges(chall_id=2, chall_name='sql_chall', chall_point=160)

        slovedchall1 = SolvedChallenges(id=0, chall_id=0, users=user1, solved_chall_name=chall1.chall_name, point=chall1.chall_point)
        slovedchall2 = SolvedChallenges(id=1, chall_id=1, users=user2, solved_chall_name=chall2.chall_name, point=chall2.chall_point)
        slovedchall3 = SolvedChallenges(id=2, chall_id=2, user_id=2, solved_chall_name=chall2.chall_name, point=chall2.chall_point)
        slovedchall4 = SolvedChallenges(id=3, chall_id=1, user_id=1, solved_chall_name=chall1.chall_name, point=chall1.chall_point)

        db.session.add_all([user1, user2])
        db.session.add_all([chall1, chall2, chall3])
        db.session.add_all([slovedchall1, slovedchall2, slovedchall3, slovedchall4])

        db.session.commit()

