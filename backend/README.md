Walidacja w aplikacji
Walidacja podczas tworzenia rezerwacji: W momencie tworzenia nowej rezerwacji, należy sprawdzić, czy przekazano przynajmniej jeden Table:
python
Skopiuj kod
def create_reservation(session, reservation_data, table_ids):
    if not table_ids or len(table_ids) < 1:
        raise ValueError("Reservation must include at least one table.")
    
    # Pobierz stoliki z bazy danych
    tables = session.query(Table).filter(Table.id.in_(table_ids)).all()

    if len(tables) != len(table_ids):
        raise ValueError("One or more tables do not exist.")

    # Sprawdź, czy stoliki nie są już przypisane do innych rezerwacji
    for table in tables:
        if table.reservation_id is not None:
            raise ValueError(f"Table {table.number} is already reserved.")

    # Utwórz rezerwację i przypisz stoliki
    reservation = Reservation(**reservation_data)
    reservation.tables = tables

    session.add(reservation)
    session.commit()


Przykład użycia w FastAPI
python
Skopiuj kod
@app.post("/reservations/")
def create_reservation_endpoint(reservation: ReservationSchema, table_ids: List[int], db: Session = Depends(get_db)):
    try:
        create_reservation(db, reservation.dict(), table_ids)
        return {"message": "Reservation created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

