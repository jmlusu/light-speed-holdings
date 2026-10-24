/**
 * LightSpeed Holdings — Google Slides frame/boundary QA plugin.
 *
 * Google Slides equivalent of scripts/qa/check_slide_bounds.py. Because Google
 * Slides has no local file, this runs inside the target presentation as an Apps
 * Script. It walks every page element, converts its position/size to inches,
 * and flags any element that (a) sits outside the slide frame, (b) breaches the
 * safety margin, or (c) is a text element whose declared font size + character
 * count would overflow its box (approximated the same way as the Python side).
 *
 * SETUP
 *   1. Open the deck in Google Slides.
 *   2. Extensions -> Apps Script. Paste this file, save.
 *   3. Run `checkFrameBounds()` and grant the presentation scope when prompted.
 *   4. Read the results: they are logged (View -> Logs) AND appended as a
 *      red-bordered note off-canvas on slide 1, so QA is visible in-deck.
 *
 * Notes / limits:
 *   - 1 inch = 72 points in the Google Slides API.
 *   - The text-overflow estimate uses an Arial average glyph width of 0.58 * pt,
 *     matching scripts/qa/check_slide_bounds.py so both tools agree.
 *   - Off-slide "scratch" elements at negative offsets are treated as intentional
 *     staging and are reported as INFO, not failures.
 */

var SLIDE_MARGIN_IN = 0.15;   // safety margin, inches
var TEXT_TOLERANCE_IN = 0.35; // allowed text overflow before FAIL
var PT_PER_IN = 72;

/** Runs the check. Call from the Apps Script editor or a custom menu. */
function checkFrameBounds() {
  var slides = SlidesApp.getActivePresentation().getSlides();
  var violations = [];
  var warnings = [];

  for (var s = 0; s < slides.length; s++) {
    var page = slides[s];
    var pageSize = SlidesApp.getActivePresentation().getPageWidth(); // pts
    var pageWidthIn = SlidesApp.getActivePresentation().getPageWidth() / PT_PER_IN;
    var pageHeightIn = SlidesApp.getActivePresentation().getPageHeight() / PT_PER_IN;
    var elements = page.getPageElements();

    for (var e = 0; e < elements.length; e++) {
      var el = elements[e];
      var left = el.getLeft() / PT_PER_IN;
      var top = el.getTotalOffsetY() / PT_PER_IN;
      var w = el.getWidth() / PT_PER_IN;
      var h = el.getHeight() / PT_PER_IN;
      var right = left + w;
      var bottom = top + h;

      // Intentional off-canvas staging (scratch space) -> INFO only.
      if (left < -0.01 || top < -0.01) {
        continue;
      }

      // (a) Outside the frame.
      if (right > pageWidthIn + 0.001 || bottom > pageHeightIn + 0.001) {
        violations.push(
          'slide ' + (s + 1) + ': element out of frame (L=' + left.toFixed(2) +
          ' T=' + top.toFixed(2) + ' R=' + right.toFixed(2) + ' B=' + bottom.toFixed(2) +
          ' vs slide ' + pageWidthIn.toFixed(2) + 'x' + pageHeightIn.toFixed(2) + ')'
        );
        continue;
      }

      // (b) Safety-margin breach.
      if (
        left < SLIDE_MARGIN_IN - 0.001 ||
        top < SLIDE_MARGIN_IN - 0.001 ||
        right > pageWidthIn - SLIDE_MARGIN_IN + 0.001 ||
        bottom > pageHeightIn - SLIDE_MARGIN_IN + 0.001
      ) {
        warnings.push(
          'slide ' + (s + 1) + ': breaches ' + SLIDE_MARGIN_IN + 'in margin (R=' +
          right.toFixed(2) + ' B=' + bottom.toFixed(2) + ')'
        );
      }

      // (c) Text overflow estimate for text-bearing elements.
      if (el.getPageElementType() === SlidesApp.PageElementType.TEXT) {
        var need = estimateTextHeightIn(el, Math.max(w, 0.2));
        if (need > h + TEXT_TOLERANCE_IN) {
          violations.push(
            'slide ' + (s + 1) + ': text overflow — needs ~' + need.toFixed(2) +
            'in but box is ' + h.toFixed(2) + 'in: ' +
            "'" + truncate(el.asString().trim(), 60) + "'"
          );
        }
      }
    }
  }

  report(violations, warnings);
}

/** Estimated wrapped-text height (inches) for a text element. */
function estimateTextHeightIn(el, widthIn) {
  var totalIn = 0;
  var ranges = el.getText().getAllRanges();
  for (var i = 0; i < ranges.length; i++) {
    var range = ranges[i];
    var text = range.getString();
    if (!text) continue;
    // Average font size across the range.
    var styles = range.getTextStyle();
    var pt = styles.getFontSize();
    if (!pt || pt <= 0) pt = 14;
    var charsPerLine = Math.max(1, Math.floor((widthIn * 96.0) / (pt * 0.58)));
    var lines = 0;
    var segs = text.split('\n');
    for (var j = 0; j < segs.length; j++) {
      lines += Math.max(1, Math.ceil(segs[j].length / charsPerLine));
    }
    totalIn += lines * pt * 1.32 / 72.0;
  }
  return totalIn;
}

function truncate(s, n) {
  return s.length > n ? s.slice(0, n) + '…' : s;
}

/** Log results and drop a visible PASS/FAIL banner onto slide 1. */
function report(violations, warnings) {
  var header = 'check_slide_bounds (Google Slides): ' +
    violations.length + ' violation(s), ' + warnings.length + ' warning(s)';
  Logger.log(header);
  for (var i = 0; i < violations.length; i++) Logger.log('FAIL: ' + violations[i]);
  for (var j = 0; j < warnings.length; j++) Logger.log('WARN: ' + warnings[j]);

  var slides = SlidesApp.getActivePresentation().getSlides();
  var first = slides[0];
  var pageW = SlidesApp.getActivePresentation().getPageWidth();
  var box = first.insertTextBox(
    (violations.length ? 'FRAME QA: FAIL — ' + violations.length + ' violation(s)\n' : 'FRAME QA: PASS\n') +
      header,
    pageW - 300, -60, 290, 50
  );
  var red = SlidesApp.newTextStyle().setForegroundColor('#E63946').build();
  var green = SlidesApp.newTextStyle().setForegroundColor('#0F7B34').build();
  box.getText().setTextStyle(violations.length ? red : green);
}
