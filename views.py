from datetime import datetime

from origina_framework.responce import Status
from origina_framework.templator import render
from patterns.behavioral_patterns import BaseSerializer, EmailNotifier, SmsNotifier, ListView, CreateView
from patterns.creational_patterns import Engine, Logger, Student
from patterns.structural_patterns import AppRoute, Debug

routes = {}
site = Engine()
logger = Logger("main")
email_notifier = EmailNotifier
sms_notifier = SmsNotifier


class NotFound404:
    @Debug(name="404")
    def __call__(self, request):
        return Status.HTTP_404_NOT_FOUND()


@AppRoute(routes=routes, url="/")
class Index:
    @Debug(name="Index")
    def __call__(self, request):
        return Status.HTTP_200_OK(), render("index.html")


@AppRoute(routes=routes, url="/portfolio/")
class Portfolio:
    @Debug(name="Portfolio")
    def __call__(self, request):
        return Status.HTTP_200_OK(), render("portfolio.html")


@AppRoute(routes=routes, url="/services/")
class Services:
    @Debug(name="Services")
    def __call__(self, request):
        return Status.HTTP_200_OK(), render("services.html")


@AppRoute(routes=routes, url="/study_programs/")
class StudyPrograms:
    @Debug(name="Programs")
    def __call__(self, request):
        return Status.HTTP_200_OK(), render(
            "study-programs.html", date=datetime.now()
        )


@AppRoute(routes=routes, url="/courses-list/")
class CoursesList:
    @Debug(name="Course list")
    def __call__(self, request):
        logger.log("Список курсов")
        try:
            category = site.find_category_by_id(
                int(request["request_params"]["id"])
            )
            return Status.HTTP_200_OK(), render(
                "course_list.html",
                objects_list=category.courses,
                name=category.name,
                id=category.id,
            )
        except KeyError:
            return Status.HTTP_200_OK(), render(
                "course_list.html",
                say="Курсы еще не добавлены",
            )


@AppRoute(routes=routes, url="/create-course/")
class CreateCourse:
    category_id = -1

    @Debug(name="Create course")
    def __call__(self, request):
        if request["method"] == "POST":
            data = request["data"]

            name = data["name"]
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course("record", name, category)
                site.courses.append(course)

            return Status.HTTP_200_OK(), render(
                "course_list.html",
                objects_list=category.courses,
                name=category.name,
                id=category.id,
            )

        else:
            try:
                self.category_id = int(request["request_params"]["id"])
                category = site.find_category_by_id(int(self.category_id))

                return Status.HTTP_200_OK(), render(
                    "create_course.html", name=category.name, id=category.id
                )
            except KeyError:
                return Status.HTTP_200_OK(), render(
                    "create_course.html", say="Категории еще не добавлены"
                )


@AppRoute(routes=routes, url="/create-category/")
class CreateCategory:
    @Debug(name="Create category")
    def __call__(self, request):

        if request["method"] == "POST":
            print(request)
            data = request["data"]

            name = data["name"]
            name = site.decode_value(name)

            category_id = data.get("category_id")

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return Status.HTTP_200_OK(), render(
                "index.html", objects_list=site.categories
            )
        else:
            categories = site.categories
            return Status.HTTP_200_OK(), render(
                "create_category.html", categories=categories
            )


@AppRoute(routes=routes, url="/category-list/")
class CategoryList:
    @Debug(name="Category list")
    def __call__(self, request):
        logger.log("Список категорий")
        return Status.HTTP_200_OK(), render(
            "category_list.html", objects_list=site.categories
        )


@AppRoute(routes=routes, url="/copy-course/")
class CopyCourse:
    @Debug(name="Copy course")
    def __call__(self, request):
        request_params = request["request_params"]

        try:
            name = request_params["name"]
            old_course = site.get_course(name)
            if old_course:
                new_name = f"copy_{name}"
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
            return Status.HTTP_200_OK(), render(
                "course_list.html", objects_list=site.courses
            )
        except KeyError:
            return Status.HTTP_200_OK()


class FakeViews:
    @Debug(name="Fake")
    def __call__(self):
        return Status.HTTP_200_OK_FAKE()


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()


@AppRoute(routes=routes, url="/student-list/")
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url="/create-student/")
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url="/add-student")
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)