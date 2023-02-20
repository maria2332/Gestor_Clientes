from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator
import database as db
import helpers


headers = {"content-type": "charset=utf-8"} # Para que los caracteres especiales se muestren correctamente


class ModeloCliente(BaseModel): #creamos la clase ModeloCliente que hereda de BaseModel
    dni: constr(min_length=3, max_length=3) #creamos los atributos dni, nombre y apellido con restricciones de longitud mínima y máxima
    nombre: constr(min_length=2, max_length=30)
    apellido: constr(min_length=2, max_length=30)


class ModeloCrearCliente(ModeloCliente): #creamos la clase ModeloCrearCliente que hereda de ModeloCliente
    @validator("dni") #creamos el validador dni
    def validar_dni(cls, dni): #creamos el método validar_dni con el parámetro dni
        if not helpers.dni_valido(dni, db.Clientes.lista): #si el dni no es válido, se lanza una excepción
            raise ValueError("Cliente ya existente o DNI incorrecto") 
        return dni


app = FastAPI( 
    title="API del Gestor de clientes",     
    description="Ofrece diferentes funciones para gestionar los clientes.") 


@app.get("/clientes/", tags=["Clientes"])   #creamos la ruta /clientes/ con el método GET
async def clientes():   
    content = [cliente.to_dict() for cliente in db.Clientes.lista]      
    return JSONResponse(content=content, headers=headers)


@app.get("/clientes/buscar/{dni}/", tags=["Clientes"]) #creamos la ruta /clientes/buscar/ con el método GET
async def clientes_buscar(dni: str):
    cliente = db.Clientes.buscar(dni=dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=headers)


@app.post("/clientes/crear/", tags=["Clientes"]) #creamos la ruta /clientes/crear/ con el método POST
async def clientes_crear(datos: ModeloCrearCliente):
    cliente = db.Clientes.crear(datos.dni, datos.nombre, datos.apellido)
    if cliente:
        return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)


@ app.put("/clientes/actualizar/", tags=["Clientes"]) #creamos la ruta /clientes/actualizar/ con el método PUT
async def clientes_actualizar(datos: ModeloCliente):
    if db.Clientes.buscar(datos.dni):
        cliente = db.Clientes.modificar(datos.dni, datos.nombre, datos.apellido)
        if cliente:
            return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)


@app.delete("/clientes/borrar/{dni}/", tags=["Clientes"]) #creamos la ruta /clientes/borrar/ con el método DELETE
async def clientes_borrar(dni: str):
    if db.Clientes.buscar(dni=dni):
        cliente = db.Clientes.borrar(dni=dni)
        return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)

print("Servidor de la API...") 
