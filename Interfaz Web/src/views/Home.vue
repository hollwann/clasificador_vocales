<template>
  <v-container grid-list-xl fill-height>
    <v-layout row wrap>
      <v-flex
        xs12
        md8
        offset-md2
        text-xs-center
        elevation-1
        style="background:white"
      >
        <h1 class="display-3">Clasificador de vocales</h1>
        <h2 class="headline">Alzate Herrera - Barrera Barreto León</h2>

        <v-container pt-5 class="text-xs-center">
          <v-btn round color="primary" large dark @click="startMic">{{
            btnMessage
          }}</v-btn>
        </v-container>

        <h3 class="display-1">{{ predictedVowel }}</h3>
        <h3>{{ predPercentage * 100 }}%</h3>
        <template v-for="(item, idx) in predVowels">
          <p :key="idx">{{ item }}</p>
        </template>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import * as tf from '@tensorflow/tfjs'
import { R } from '@/services/resampler.js'
import util from '@/services/util.js'

export default {
  data() {
    return {
      predictedVowel: '',
      predPercentage: 0,
      predVowels: [],
      btnMessage: 'Pulsa para comenzar'
    }
  },
  methods: {
    startMic() {
      this.btnMessage = 'Cargando...'
      this.predVowels = []
      var that = this
      navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then(async stream => {
          let context = new AudioContext(),
            bufSize = 16384,
            microphone = context.createMediaStreamSource(stream),
            processor = context.createScriptProcessor(bufSize, 1, 1),
            res = new R(context.sampleRate, 8000, 1, bufSize),
            bufferArray = []

          processor.onaudioprocess = event => {
            // const right = event.inputBuffer.getChannelData(1);
            const outBuf = res.resample(event.inputBuffer.getChannelData(0))
            bufferArray.push.apply(bufferArray, outBuf)
          }

          this.start = () => {
            if (processor && microphone) {
              bufferArray = []
              microphone.connect(processor)
              processor.connect(context.destination)
            }
          }

          this.stop = () => {
            if (processor && microphone) {
              microphone.disconnect()
              processor.disconnect()
            }
          }

          this.getPcm = () => {
            return new Float32Array(bufferArray)
          }
          this.get16BitPcm = () => {
            //floatTo16BitPCM  in util.js file
            return util.floatTo16BitPCM(bufferArray)
          }
          tf.setBackend('cpu')
          console.log('cargando modelo.')
          try {
            const model = await tf.loadLayersModel(
              'https://predictori.web.app/tf/model.json'
            )
            console.log('modelo cargado')
            that.btnMessage = 'Habla!'
            // eslint-disable-next-line no-constant-condition
            while (true) {
              try {
                this.start()
                await util.sleep(300)
                this.stop()
                var pred = util.predict_vowel(this.get16BitPcm(), model)
                if (pred[0] != '') {
                  if (pred[0] != that.predictedVowel) {
                    that.predictedVowel = pred[0]
                    that.predVowels.push(pred[0])
                  }
                  that.predPercentage = pred[1]
                }
              } catch (e) {
                null
              }
            }
          } catch (e) {
            this.predictedVowel =
              'No se pudo cargar el modelo, revisa tu conexión.'
          }
        })
    }
  }
}
</script>

<style scoped></style>
