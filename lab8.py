from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, Session, relationship

engine = create_engine('sqlite:///settings.db', echo=False)
Base = declarative_base()

class Settings(Base):
    __tablename__ = 'Settings'

    Id = Column(Integer, primary_key=True)
    SettingName = Column(String)
    SettingValue = Column(String)

Base.metadata.create_all(engine)

def create_session():
    return Session(engine)

def create_setting(session, name, value):
    new_setting = Settings(SettingName=name, SettingValue=value)
    session.add(new_setting)
    session.commit()

def get_all_settings(session):
    return session.query(Settings).all()

def update_setting(session, id, new_name, new_value):
    setting_to_update = session.query(Settings).filter_by(Id = id).first()
    if setting_to_update:
        setting_to_update.SettingName = new_name
        setting_to_update.SettingValue = new_value
        session.commit()

def delete_setting(session, id):
    setting_to_delete = session.query(Settings).filter_by(Id=id).first()
    if setting_to_delete:
        session.delete(setting_to_delete)
        session.commit()

def get_settings_filtered(session, value):
    query = session.query(Settings.SettingName, Settings.SettingValue)

    if value:
        query = query.filter(Settings.SettingValue == value)

    return query.all()

def total_setting_per_value(session):
    return session.query(Settings.SettingValue, func.count(Settings.SettingName).label('total_values')).\
        group_by(Settings.SettingValue).all()


def close_session(session):
    session.close()

session = create_session()

# settings_to_add = [['VSync', "On"],['Resolution', "1280X1920"], ['Motion Blur', "On"]]
# for item in settings_to_add:
#     create_setting(session, item[0], item[1])

all_settings = get_all_settings(session)
print("All Settings:")
for setting in all_settings:
    print(setting.Id + "|" + setting.SettingName + "|" + setting.SettingValue)

medium_quality = get_settings_filtered(session, "Medium")
print("\nMedium settings:")
for order in medium_quality:
    print(f"{order[0]} | {order[1]}")

total_settings = total_setting_per_value(session)
print("\nTotal:")
for row in total_settings:
    print(row)

close_session(session)
