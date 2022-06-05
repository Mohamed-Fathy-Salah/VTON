import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import * as dat from 'dat.gui'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js'
import { Material, ObjectLoader } from 'three'


/**
 * Loaders
 */
const objLoader = new OBJLoader()
const textureLoader = new THREE.TextureLoader()
const mtlLoader = new MTLLoader()

// Debug
const gui = new dat.GUI()
const debugObject = {}

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()


const skinTones = {
    'male':{
        'african': '/textures/skin_tones/male/skin_m_african.png',
        'asian': '/textures/skin_tones/male/skin_m_asian.png',
        'hispanic': '/textures/skin_tones/male/skin_m_hispanic.png',
        'indian': '/textures/skin_tones/male/skin_m_indian.png',
        'mideast': '/textures/skin_tones/male/skin_m_mideast.png',
        'seasian': '/textures/skin_tones/male/skin_m_seasian.png',
        'white': '/textures/skin_tones/male/skin_m_white.png',   
    },
    'female':{
        'african': '/textures/skin_tones/female/skin_f_african.png',
        'asian': '/textures/skin_tones/female/skin_f_asian.png',
        'hispanic': '/textures/skin_tones/female/skin_f_hispanic.png',
        'mideast': '/textures/skin_tones/female/skin_f_mideast.png',
        'seasian': '/textures/skin_tones/female/skin_f_seasian.png',
        'white': '/textures/skin_tones/female/skin_f_white.png',
    }
}

const tshirtTex = './models/test/tex.png' 


const mtl = {

}

const body = '/models/test/body.obj'
const tshirt = '/models/test/tshirt.obj'


const skin = textureLoader.load(tshirtTex)
skin.encoding = THREE.sRGBEncoding
skin.rouphness = 1.0
skin.metalness = 0.0

const material = new THREE.MeshBasicMaterial({
    map: skin,
    // normalMap: skinNormal,
})

const depthMaterail = new THREE.MeshDepthMaterial({
    depthPacking: THREE.RGBADepthPacking,
})

objLoader.load(tshirt, (object) => {
    object.scale.set(10,10,10)
    object.position.set(0, -4, 0)
    object.rotation.y = Math.PI * 0.5

    console.log(object);

    object.traverse(function (child) {
    if (child instanceof THREE.Mesh) {
        // child.material = material
        child.material = material
        child.customDepthMaterial = depthMaterail
    }
    });

    scene.add(object);
 });


        // mtlLoader.load('/models/test/uppergar.mtl', (mat) => {
        //     mat.preload()
        //     objLoader
        //         .setMaterials(mat)
        //         .load(
        //             tshirt,
        //             function (object) {
        //                 object.scale.set(10,10,10)
        //                 object.position.set(0, -4, 0)
        //                 object.rotation.y = Math.PI * 0.5
                        
                        
        //                 object.traverse(function (child) {
        //                     if (child instanceof THREE.Mesh) {
        //                         child.material = material
        //                         child.customDepthMaterial = depthMaterail
        //                     }
        //                 });
        //                 scene.add(object);
        //         })});


/**
 * Lights
 */
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
scene.add(ambientLight)
const directionalLight = new THREE.DirectionalLight('#ffffff', 0.5)
directionalLight.castShadow = true
directionalLight.shadow.camera.far = 15
directionalLight.shadow.mapSize.set(1024, 1024)
directionalLight.shadow.normalBias = 0.05
directionalLight.position.set(5, 0.074, - 3.936)
scene.add(directionalLight)


gui.add(ambientLight, 'intensity').min(0).max(1).step(0.001).name('lightIntensity-ambient')
gui.add(directionalLight, 'intensity').min(0).max(10).step(0.001).name('lightIntensity')
gui.add(directionalLight.position, 'x').min(- 5).max(5).step(0.001).name('lightX')
gui.add(directionalLight.position, 'y').min(- 5).max(5).step(0.001).name('lightY')
gui.add(directionalLight.position, 'z').min(- 5).max(5).step(0.001).name('lightZ')

/**
 * Sizes
 */
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () =>
{
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100)
camera.position.set(4, 1, - 4)
scene.add(camera)

// Controls
const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true
})
renderer.physicallyCorrectLights = true
renderer.outputEncoding = THREE.sRGBEncoding
renderer.toneMapping = THREE.ReinhardToneMapping
renderer.toneMappingExposure = 3
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFSoftShadowMap
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

gui
    .add(renderer, 'toneMapping', {
        No: THREE.NoToneMapping,
        Linear: THREE.LinearToneMapping,
        Reinhard: THREE.ReinhardToneMapping,
        Cineon: THREE.CineonToneMapping,
        ACESFilmic: THREE.ACESFilmicToneMapping
    })
    .onFinishChange(() =>
    {
        renderer.toneMapping = Number(renderer.toneMapping)
        updateAllMaterials()
    })
gui.add(renderer, 'toneMappingExposure').min(0).max(10).step(0.001)

/**
 * Animate
 */
const tick = () =>
{
    // Update controls
    controls.update()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()