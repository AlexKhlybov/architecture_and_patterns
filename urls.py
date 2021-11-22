from views import (CategoryList, CopyCourse, CoursesList, CreateCategory,
                   CreateCourse, Index, Portfolio, Services, StudyPrograms)

routes = {
    "/": Index(),
    "/portfolio/": Portfolio(),
    "/services/": Services(),
    "/study_programs/": StudyPrograms(),
    "/courses-list/": CoursesList(),
    "/create-course/": CreateCourse(),
    "/create-category/": CreateCategory(),
    "/category-list/": CategoryList(),
    "/copy-course/": CopyCourse(),
}
