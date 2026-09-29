"""
usuario_repository.py
---------------------
Repositorio de datos para Usuarios del Sistema.
Maneja operaciones de lectura y persistencia usando consultas SQL parametrizadas.
"""

from typing import Optional, List
from database import get_connection
from models.usuario import Usuario


class UsuarioRepository:
    def get_by_username(self, username: str) -> Optional[Usuario]:
        """Busca un usuario por su nombre de usuario (case-insensitive)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password_hash, role, active
            FROM usuarios_sistema
            WHERE LOWER(username) = LOWER(?);
        """, (username.strip(),))
        row = cursor.fetchone()
        conn.close()
        return Usuario.from_row(row) if row else None

    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su identificador primario."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password_hash, role, active
            FROM usuarios_sistema
            WHERE id = ?;
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()
        return Usuario.from_row(row) if row else None

    def list_all(self) -> List[Usuario]:
        """Retorna todos los usuarios registrados."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password_hash, role, active
            FROM usuarios_sistema
            ORDER BY id ASC;
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Usuario.from_row(r) for r in rows]

    def create(self, usuario: Usuario) -> int:
        """Registra un nuevo usuario en el sistema."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios_sistema (username, password_hash, role, active)
            VALUES (?, ?, ?, ?);
        """, (usuario.username.strip(), usuario.password_hash, usuario.role, int(usuario.active)))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id
