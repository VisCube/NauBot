from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Enum
from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum

from .database import Base


class RoleEnum(PyEnum):
    unregistered = "Незарегистрированный"
    participant = "Участник"
    admin = "Админ"
    organizer = "Организатор"
    volunteer = "Волонтер"


class SurveyTypeEnum(PyEnum):
    open = "Открытый"
    options = "С вариантами ответа"


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)

    registrations: Mapped[List["Registration"]] = relationship(back_populates="user", cascade="all, delete")
    sent_questions: Mapped[List["Question"]] = relationship(back_populates="sender", cascade="all, delete")
    speaker_masterclasses: Mapped[List["Masterclass"]] = relationship(back_populates="speaker",
                                                                      foreign_keys="[Masterclass.speaker_id]")


class Masterclass(Base):
    __tablename__ = "masterclasses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), nullable=False)

    speaker: Mapped[User] = relationship(back_populates="speaker_masterclasses")
    registrations: Mapped[List["Registration"]] = relationship(back_populates="masterclass", cascade="all, delete")
    questions: Mapped[List["Question"]] = relationship(back_populates="masterclass", cascade="all, delete")
    surveys: Mapped[List["Survey"]] = relationship(back_populates="masterclass", cascade="all, delete")

    @property
    def remaining_places(self) -> int:
        if not hasattr(self, "registrations") or self.registrations is None:
            return self.capacity
        registered = sum(1 for r in self.registrations if not r.is_waiting_list)
        return max(self.capacity - registered, 0)


class Registration(Base):
    __tablename__ = "registrations"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), primary_key=True)
    masterclass_id: Mapped[int] = mapped_column(ForeignKey("masterclasses.id"), primary_key=True)
    is_waiting_list: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user: Mapped[User] = relationship(back_populates="registrations")
    masterclass: Mapped[Masterclass] = relationship(back_populates="registrations")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    masterclass_id: Mapped[Optional[int]] = mapped_column(ForeignKey("masterclasses.id"), nullable=True)
    is_answered: Mapped[bool] = mapped_column(default=False)
    answer_text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    sender: Mapped[User] = relationship(back_populates="sent_questions")
    masterclass: Mapped[Optional[Masterclass]] = relationship(back_populates="questions")


class Survey(Base):
    __tablename__ = "surveys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    masterclass_id: Mapped[Optional[int]] = mapped_column(ForeignKey("masterclasses.id"), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[SurveyTypeEnum] = mapped_column(Enum(SurveyTypeEnum), nullable=False)

    masterclass: Mapped[Optional[Masterclass]] = relationship(back_populates="surveys")
    options: Mapped[List["SurveyOption"]] = relationship(back_populates="survey", cascade="all, delete")
    answers: Mapped[List["SurveyAnswer"]] = relationship(back_populates="survey", cascade="all, delete")


class SurveyOption(Base):
    __tablename__ = "survey_options"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    survey_id: Mapped[int] = mapped_column(ForeignKey("surveys.id"))
    text: Mapped[str] = mapped_column(String, nullable=False)

    survey: Mapped["Survey"] = relationship(back_populates="options")


class SurveyAnswer(Base):
    __tablename__ = "survey_answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    survey_id: Mapped[int] = mapped_column(ForeignKey("surveys.id"))
    option_id: Mapped[Optional[int]] = mapped_column(ForeignKey("survey_options.id"), nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    survey: Mapped["Survey"] = relationship(back_populates="answers")
    option: Mapped[Optional["SurveyOption"]] = relationship()
