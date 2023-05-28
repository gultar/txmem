const gulp = require('gulp');
const sass = require('gulp-sass');

// Define a task to compile SCSS to CSS
gulp.task('scss', function () {
  return gulp
    .src('./src/index.scss') // Update the path to your main SCSS file
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./src/index.css')); // Update the path to your CSS output directory
});

// Define a task to watch SCSS files and trigger the 'scss' task on changes
gulp.task('watch', function () {
  gulp.watch('./src/*.scss', gulp.series('scss')); // Update the path to your SCSS files
});

// Define a default task that runs the 'scss' task
gulp.task('default', gulp.series('scss'));
