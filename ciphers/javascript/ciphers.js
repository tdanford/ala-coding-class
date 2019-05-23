
function take(stream, n) {
  var taken = [];
  for (var i = 0; i < n; i++) {
    taken.push(stream.first);
    stream = stream.rest();
  }

  return [ taken, stream ];
}

function takeUntil(predicate, stream) {
  var taken = [];
  while (!predicate(stream.first)) {
    taken.push(stream.first);
    stream = stream.rest();
  }

  return [taken, stream];
}

function zip(stream1, stream2) {
  return createStream(
    [stream1.first, stream2.first],
    function() {
      return zip(stream1.rest(), stream2.rest());
    }
  );
}

function findFirst(predicate, stream) {
  var skippedValue = null;
  while(!predicate(stream.first)) {
    [ skippedValue, stream ] = take(stream, 1);
  }

  return stream;
}

function filter(predicate, stream) {
  stream = findFirst(predicate, stream);
  return createStream(stream.first, function() { filter(predicate, stream.rest); });
}

function range(lower, upper) {
  function next(i) {
    return createStream(
      i,
      function() {
        if ( i !== undefined && i < upper ) {
          return next(i + 1);
        } else {
          return constant(undefined);
        }
      }
    )
  }

  return next(lower);
}

function constant(k) {
  return createStream(k, function() { return constant(k); });
}

function map(f, stream) {
  return createStream(
    f(stream.first),
    () => map(f, stream.rest())
  );
}

function createStream(first, rest) {
  return {
    'first': first,
    'rest': rest
  }
}

module.exports.take = take;
module.exports.takeUntil = takeUntil;
module.exports.zip = zip;
module.exports.findFirst = findFirst;
module.exports.filter = filter
module.exports.range = range;
module.exports.constant = constant;
module.exports.map = map;
module.exports.createStream = createStream;

/**
 * We're only going to encode lower-case letters (and spaces),
 * and we'll ignore all other characters.
 */
const alphabet = ' abcdefghijklmnopqrstuvwxyz';

/**
 * Generates a random integer between [start, end)
 */
function randomInt(start, end) {
  return Math.floor(Math.random() * (end-start)) + start;
}

/**
 * Generates the index (offset) of the letter in the alphabet.
 *
 * This function ignores the case (upper or lower) of the letter
 *
 * For example:
 *   encodeLetter(' ') === 0
 *   encodeLetter('a') === 1
 *   encodeLetter('A') === 1
 *   encodeLetter('c') === 3
 *   encodeLetter('z') === 26
 *   encodeLetter('Z') === 26
 *
 */
function encodeLetter(letter) {
  return alphabet.indexOf(letter.toLowerCase());
}

function encipherLetter(offset, letter) {
  if (letter.length > 0) {
    var shifted = encodeLetter(letter) + offset;
    var encodedIdx = shifted >= 0 ?
      shifted % alphabet.length :
      alphabet.length + (shifted % alphabet.length);

    return alphabet[encodedIdx];
  } else {
    return letter;
  }
}

function encipheredStream(keyStream, stringStream) {
  return map((x) => encipherLetter(x[1], x[0]), zip(stringStream, keyStream));
}

function decipheredStream(keyStream, stringStream) {
  return encipheredStream(map((x) => -x, keyStream), stringStream);
}

/**
 *  Turns a string (the plaintext) into another string (the ciphertext) using a key.
 */
function encipher(keyStream, string_value) {
  return joined(encipheredStream(keyStream, stringStream(string_value, 1)));
}

/**
 *  Turns a string (the ciphertext) into another string (the plaintext) using a key.
 *
 *  Assuming this is the key the ciphertext was enciphered with, then the returned
 *  plaintext will be equal to the original plaintext.
 */
function decipher(keyStream, string_value) {
  return joined(decipheredStream(keyStream, stringStream(string_value, 1)));
}

/**
 *  Helper function to turn a stream-of-strings into a single string
 */
function joined(stringStream) {
  return takeUntil(
    (x) => x.length === 0,
    stringStream
  )[0].reduce((x, y) => x.concat(y));
}

/**
 *  Helper function to turn a string into a stream-of-strings, k letters at a time
 *
 *  By default (k=1), this turns a string into a stream of single letters.
 */
function stringStream(str_value, k=1) {
  return createStream(
    str_value.slice(0, k),
    function() {
      return stringStream(str_value.substring(k), k);
    }
  );
}

/**
 *  Chooses a random key for use in the Caesar cipher.
 *  (A number between [1, alphabet.length) -- this means that, since
 *  '0' is never chosen as a key, the ciphertext is never equal to the
 *  plaintext.
 */
function createCaesarKey() {
  const key = randomInt(1, alphabet.length);
  return constant(key);
}

function changingCaesarKey(startingKey, offset) {
  return createStream(
    startingKey,
    function() {
      return changingCaesarKey(
        (startingKey + offset) % alphabet.length,
        offset
      );
    }
  );
}

function createChangingCaesarKey() {
  const startingKey = randomInt(1, alphabet.length);
  const offset = randomInt(1, alphabet.length);

  return changingCaesarKey(startingKey, offset);
}

module.exports.encipherLetter = encipherLetter;
module.exports.encipheredStream = encipheredStream;
module.exports.encipher = encipher;
module.exports.decipher = decipher;
module.exports.joined = joined;
module.exports.stringStream = stringStream;
module.exports.randomInt = randomInt;
module.exports.createChangingCaesarKey = createChangingCaesarKey;
module.exports.createCaesarKey = createCaesarKey;
