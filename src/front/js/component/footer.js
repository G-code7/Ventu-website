import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../../static/images/ventu-logo.png';

export const Footer = () => (
    <footer className="footer mt-auto py-3 text-center " style={{ backgroundColor: '#00B4E7', color: '#FFF' }}>
        <div className="container">
            <div className="row">
                
                {/* Columna izquierda */}
                <div className="col-12 col-md-6 text-start">
                    {/* Logo */}
                    <img src={logo} alt="Ventu Logo" style={{ width: '150px', height: 'auto' }} />
                    
                    {/* CTA */}
                    <h4 className="mt-3 text-black"></h4>
                    <p className='text-black'></p>
                </div>

                {/* Columna derecha */}
                <div className="col-12 col-md-6 mt-4 mt-4 md-0 text-end pe-0">
                    {/* Título del menú */}
                    <h4 className="mb-1 col-11 pe-2 text-black">Menú</h4>

                    {/* Menú */}
                    <nav className="d-flex flex-column col-11 pe-0">
                        <Link to="/" className="btn btn-link text-black text-end">Inicio</Link>
                        <Link to="/tourplans" className="btn btn-link text-black text-end">Planes Turísticos</Link>
                        <Link to="/about" className="btn btn-link text-black text-end">Sobre Nosotros</Link>
                        <Link to="/creartourplan" className="btn btn-link text-black text-end">Crear Plan Turístico</Link>
                    </nav>
                </div>
            </div>
            
            {/* Derechos reservados */}
            <div className="row mt-4">
                <div className="col-12 text-center">
                    <span>© 2024 Ventu. Todos los derechos reservados.</span>
                </div>
            </div>
        </div>
    </footer>
);
