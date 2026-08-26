from models import SessionLocal, User, WrongNote
import bcrypt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(db, username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(username=username, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return user
    return None

def save_wrong_note(db, user_id, question_text, standard_answer, error_analysis, knowledge_points, tags, image_path=None, mastery_level=None):
    note = WrongNote(
        user_id=user_id,
        question_text=question_text,
        standard_answer=standard_answer,
        error_analysis=error_analysis,
        knowledge_points=knowledge_points,
        tags=tags,
        original_image=image_path,
        mastery_level=mastery_level or "未掌握"
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes_by_user(db, user_id, tag=None):
    query = db.query(WrongNote).filter(WrongNote.user_id == user_id)
    if tag:
        query = query.filter(WrongNote.tags.contains(tag))
    return query.order_by(WrongNote.created_at.desc()).all()

def update_mastery(db, note_id, level):
    note = db.query(WrongNote).filter(WrongNote.id == note_id).first()
    if note:
        note.mastery_level = level
        db.commit()
        return note
    return None

def get_stats(db, user_id):
    notes = db.query(WrongNote).filter(WrongNote.user_id == user_id).all()
    total = len(notes)
    mastered = sum(1 for n in notes if n.mastery_level == '已掌握')
    rate = (mastered / total * 100) if total > 0 else 0
    return total, mastered, rate
