const vowels = ['a', 'e', 'i', 'o', 'u']

import * as tf from '@tensorflow/tfjs'

export default {
  floatTo16BitPCM(input) {
    let i = input.length
    let output = new Int16Array(i)
    while (i--) {
      let s = Math.max(-1, Math.min(1, input[i]))
      output[i] = s < 0 ? s * 0x8000 : s * 0x7fff
    }
    return output
  },

  int16ToFloat32BitPCM(input) {
    let i = input.length
    let output = new Float32Array(i)
    while (i--) {
      let int = input[i]
      output[i] = int >= 0x8000 ? -(0x10000 - int) / 0x8000 : int / 0x7fff
    }
    return output
  },
  sleep(time) {
    return new Promise(resolve => setTimeout(resolve, time))
  },
  createTensor(t) {
    t = t.slice(0, 256)
    var max_t = Math.max(...t, 1)
    var new_t = []
    for (var i = 0; i < 256; i++) {
      new_t.push(t[i] / max_t)
    }
    return tf.tensor(new_t, [1, 256])
  },
  avg(elmt) {
    var sum = 0
    for (var i = 0; i < elmt.length; i++) {
      sum += elmt[i] //don't forget to add the base
    }
    return sum / elmt.length
  },
  occurrence(array) {
    'use strict'
    var result = {}
    if (array instanceof Array) {
      // Check if input is array.
      array.forEach(function(v, i) {
        if (!result[v]) {
          // Initial object property creation.
          result[v] = [i] // Create an array for that property.
        } else {
          // Same occurrences found.
          result[v].push(i) // Fill the array.
        }
      })
    }
    var cont = []
    for (var i = 0; i < 5; i++) {
      if (i in result) {
        cont.push(result[i].length)
      } else {
        cont.push(0)
      }
    }
    return cont
  },
  predict_vowel(data, model) {
    //console.log(data)
    const step = 8
    const window = 256
    data = Array.from(data)
    //console.log(data)
    let totalSamples = Math.floor((data.length - window) / step)
    let tensorData = []
    var sample
    var max_sample
    for (var i = 0; i < totalSamples; i++) {
      sample = data.slice(i * step, i * step + window)
      if (this.avg(sample.map(Math.abs)) > 800) {
        max_sample = Math.max(...sample, 1)
        tensorData.push(
          sample.map(function(d) {
            return d / max_sample
          })
        )
      }
    }
    if (tensorData.length > 150) {
      tensorData = tf.tensor2d(tensorData, [tensorData.length, 256])
      var prediction = model.predict(tensorData).arraySync()
      //console.log(prediction);
      var vocal_pred = prediction.map(function(d) {
        return d.indexOf(Math.max(...d))
      })
      vocal_pred = this.occurrence(vocal_pred)
      var sum = 0
      for (i = 0; i < vocal_pred.length; i++) {
        sum += vocal_pred[i]
      }
      //console.log(vocal_pred)
      return [
        vowels[vocal_pred.indexOf(Math.max(...vocal_pred))],
        Math.max(...vocal_pred) / sum
      ]
    } else {
      return ['', 0]
    }
    //console.log(vocal_pred);
  }
}
