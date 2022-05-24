import './style.css'
import * as THREE from 'three'
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js'
import * as debuger from 'lil-gui';
import { OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import { MTLLoader} from 'three/examples/jsm/loaders/MTLLoader';
import axios from 'axios';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader'

let scene, camera, clock, smpl;
let gender,garments;
const path = 'http://127.0.0.1:4000/obj/body.obj'
// const plyPath = 'http://127.0.0.1:4000/obj/body.ply'

const lowerGarPlyPath = 'http://127.0.0.1:4000/ply/lowergar.ply'
const upperGarPlYPath = 'http://127.0.0.1:4000/ply/uppergar.ply'

const gar_path_upper = 'http://127.0.0.1:4000/obj/uppergar.obj'
const gar_path_upper_tex = 'http://127.0.0.1:4000/obj/uppergar.mtl'
const gar_path_lower = 'http://127.0.0.1:4000/obj/lowergar.obj'
const gar_path_lower_tex = 'http://127.0.0.1:4000/obj/lowergar.mtl'



const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}


const canvas = document.querySelector('canvas.webgl')
clock = new THREE.Clock()

scene = new THREE.Scene()
scene.background = new THREE.Color( 0x808080 );
scene.fog = new THREE.Fog( 0xa0a0a0, 10, 50 );

const hemiLight = new THREE.HemisphereLight( 0xffffff, 0x444444 );
hemiLight.position.set( 0, 20, 0 );
scene.add( hemiLight );

const dirLight = new THREE.DirectionalLight( 0xffffff );
dirLight.position.set( 3, 10, 10 );
dirLight.castShadow = true;
dirLight.shadow.camera.top = 2;
dirLight.shadow.camera.bottom = - 2;
dirLight.shadow.camera.left = - 2;
dirLight.shadow.camera.right = 2;
dirLight.shadow.camera.near = 0.1;
dirLight.shadow.camera.far = 40;
scene.add( dirLight );

const mesh = new THREE.Mesh( new THREE.PlaneGeometry( 100, 100 ), new THREE.MeshPhongMaterial( { color: 0x808080, depthWrite: false } ) );
mesh.rotation.x = - Math.PI / 2;
mesh.receiveShadow = true;
scene.add( mesh );

const loader = new OBJLoader()
const garloader = new OBJLoader()
const mtlloader = new MTLLoader()
const mtlloader2 = new MTLLoader()
const plyLoader = new PLYLoader();

loader.load(path, function ( obj ) {
        smpl = obj
        scene.add(smpl);
        smpl.position.y = 0.8
        smpl.traverse((object)=>{
            if ( object.isMesh ) object.castShadow = true;
    });
})

loader.load(path, function ( obj ) {
    smpl = obj
    scene.add(smpl);
    smpl.position.y = 0.8
    smpl.position.x = 2
    smpl.traverse((object)=>{
        if ( object.isMesh ) object.castShadow = true;
});
})

//upper tex
mtlloader.load(gar_path_upper_tex, function ( material ) {
       material.preload();
        garloader.setMaterials(material)
    garloader.load(gar_path_upper, function ( gar ) {
            scene.add(gar);
            gar.position.y = 0.8
        //     gar.traverse((object)=>{
        //     if ( object.isMesh ) object.castShadow = true;
    });

});
//lower gar tex
mtlloader2.load(gar_path_lower_tex, function ( material ) {
   //x material.preload();
     garloader.setMaterials(material)

    garloader.load(gar_path_lower, function ( gar ) {
         scene.add(gar);
         gar.position.y = 0.8
     //     gar.traverse((object)=>{
     //     if ( object.isMesh ) object.castShadow = true;
 });

});

// plyLoader.load(plyPath, function (geometry) {
//         geometry.computeVertexNormals()
//         const material = new THREE.MeshStandardMaterial( { flatShading: true } );
//         const mesh = new THREE.Mesh(geometry, material)
//         mesh.position.y = 0.8
//         mesh.position.x = 1
//         scene.add(mesh)
//     }
// )
//lower garment
plyLoader.load(lowerGarPlyPath, function (geometry) {
    geometry.computeVertexNormals()
    const material = new THREE.MeshStandardMaterial( { flatShading: true} );
    material.vertexColors = true
    const mesh = new THREE.Mesh(geometry,material )
    mesh.position.y = 0.8
    mesh.position.x = 2
    scene.add(mesh)
}
)
//upper garment
plyLoader.load(upperGarPlYPath, function (geometry) {
    geometry.computeVertexNormals()
    const material = new THREE.MeshStandardMaterial( { flatShading: true} );
    material.vertexColors = true
    const mesh = new THREE.Mesh(geometry,material )
    mesh.position.y = 0.8
    mesh.position.x = 2
    scene.add(mesh)
}
)


// const loader2 = new PLYLoader();
// loader2.load(
//     'http://127.0.0.1:4000/obj/gar.ply',
//     function (geometry) {
//         geometry.computeVertexNormals()
//         const mesh = new THREE.Mesh(geometry, material)
//         mesh.rotateX(-Math.PI / 2)
//         scene.add(mesh)
//     },
//     (xhr) => {
//         console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
//     },
//     (error) => {
//         console.log(error)
//     }
// )


const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true
})

camera = new THREE.PerspectiveCamera(45, sizes.width / sizes.height, 0.1, 100)
camera.position.set(0,2,3) 
scene.add(camera)

renderer.setSize(sizes.width, sizes.height)
renderer.render(scene, camera)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.shadowMap.enabled = true;

const controls = new OrbitControls(camera, canvas)
controls.enablePan = false;
// controls.enableZoom = false;
controls.enableDamping = true;
controls.target.set( 0, 1, 0 );


tick()

window.addEventListener('resize', function onWindowResize(){

    // update size
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    //update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

    

const gui = new debuger.GUI({width: 310})
gui.domElement.id = 'gui';

const folder1 = gui.addFolder( 'SMPL Builder' );
const folder2 = gui.addFolder( 'garment Builder' );

const debugerParameters = {
    Height:160,
    Weight:70,
    Chest:95,
    Waist:80,
    Hips:100,
    Inseam:80,
    Shoulder_width:35,
    Show_SMPL: ()=>{  
        console.log(debugerParameters);
    axios({
        method: 'post',
        url: 'http://127.0.0.1:4000/measurments',
        data: { measurments: debugerParameters }
    }).then((res)=>{
        console.log(res);
    }).catch(error =>{
            console.log(error);
        });
    },
    Gender: 'Female',
    Pose: 'T Pose',
    // Garments: 'short-pant'
    upperGarment:'t-shirt',
    lowerGarment:'short-pant',
    upperTexture:'cotton',
    lowerTexture:'jeans'
}

// const male_garments = ['no_garment','t-shirt','short-pant']
const female_garments = ['no_garment','t-shirt','skirt','short-pant']

folder1.add(debugerParameters, 'Height', 90, 220, 0.1).name('Height (cm)')
folder1.add(debugerParameters, 'Weight', 25, 200, 0.1).name('Weight (kg)')
folder1.add(debugerParameters, 'Chest', 60, 140, 0.1).name('Chest circumference (cm)')
folder1.add(debugerParameters, 'Waist', 40, 125, 0.1).name('Waist circumference (cm)')
folder1.add(debugerParameters, 'Hips', 80, 130, 0.1).name('Hip circumference (cm)')
folder1.add(debugerParameters, 'Inseam', 60, 100, 0.1).name('Inseam (cm)')
folder1.add(debugerParameters, 'Shoulder_width', 30, 50, 0.1).name('Shoulder Width (cm)')
folder1.add(debugerParameters, 'Gender', [ 'Male', 'Female'])
folder1.add(debugerParameters, 'Pose', [ 'T Pose', 'A Pose', 'Y pose'])
folder1.add(debugerParameters, 'Show_SMPL')
 folder2.add(debugerParameters, 'upper garment',['t-shirt',"no_garment"])
 folder2.add(debugerParameters, 'lower garment',['skirt',"no_garment",'short-pant','pant'])
 folder2.add(debugerParameters, 'upper texture',['jeans','cotton'])
 folder2.add(debugerParameters, 'lower texture',['jeans','cotton'])




// folder2.add( debugerParameters, 'Garments').listen().onChange((debugerParameters.Gender) => {
//     if(debugerParameters.Gender === 'Male'){
//         debugerParameters.Garments.options(['short_pant','shirt'])
//     }
//     else {
//         debugerParameters.Garments.options(['short_pant','shirt','skirt'])
//     }
// } );


// window.addEventListener('dblclick', ()=>{
//     if(!document.fullscreenElement){
//         canvas.requestFullscreen();
//     }else{
//         document.exitFullscreen();
//     }
// })



function tick (){
    
    const elapsedTime = clock.getElapsedTime()
    controls.update()
    renderer.render(scene, camera)
    window.requestAnimationFrame(tick)


}

