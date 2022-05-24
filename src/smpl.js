const express = require('express');
const cors = require('cors');
let {PythonShell} = require('python-shell');
const fs = require("fs");

const app = express();
app.use(cors())
app.use(express.json());
app.use(express.static('src/models'));



app.post('/measurments',async(req,res)=>{
    // console.log(req.body,"is req.body");
    const m = req.body.measurments
    console.log("Measurments",m);
    let options = {
        args: [m.Chest,m.Height,m.Inseam,m.Hips,m.Shoulder_width,m.Waist,m.Weight,m.Gender,m.Pose,m.upperGarment,m.lowerGarment,m.upperTexture,m.lowerTexture]
    };
    console.log(options,"is options");

    if (fs.existsSync('src/models/obj/body.obj')) {
        try {
            fs.unlinkSync('src/models/obj/body.obj');
            console.log("File removed:", 'src/models/obj/body.obj');
        } catch (err) {
            console.error(err);
        }
      }
    
    if (fs.existsSync('src/models/obj/gar.obj')) {
        try {
            fs.unlinkSync('src/models/obj/gar.obj');
            console.log("File removed:", 'src/models/obj/gar.obj');
        } catch (err) {
            console.error(err);
        }
    }

    if (fs.existsSync('src/models/obj/gar.mtl')) {
        try {
            fs.unlinkSync('src/models/obj/gar.mtl');
            console.log("File removed:", 'src/models/obj/gar.mtl');
        } catch (err) {
            console.error(err);
        }
    }

    PythonShell.run('./src/smplBuilder.py', options , function (err,out) {
        console.log('finished run')
        if (err) {
            console.log(err);
        }
        
     return res.status(200).send('http://127.0.0.1:4000/obj/body.obj')
    })

});


app.listen(4000,()=>{
    console.log("Server is running on port 4000");
})
