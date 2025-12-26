from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_db
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService
from app.monitoring.metrics import (
    items_operations_total,
    DatabaseQueryTimer
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste des items avec pagination."""
    
    try:
        # Mesurer la durée de la requête DB
        with DatabaseQueryTimer():
            items = ItemService.get_all(db, skip, limit)
        
        #  Incrémenter le compteur après succès
        items_operations_total.labels(operation='read', status='success').inc()
        
        return items
    except Exception as e:
        items_operations_total.labels(operation='read', status='error').inc()
        raise


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Récupère un item par son ID."""
    
    try:
        with DatabaseQueryTimer():
            item = ItemService.get_by_id(db, item_id)
        
        if not item:
            items_operations_total.labels(operation='read', status='not_found').inc()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        
        items_operations_total.labels(operation='read', status='success').inc()
        return item
    except HTTPException:
        raise
    except Exception as e:
        items_operations_total.labels(operation='read', status='error').inc()
        raise


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    """Crée un nouvel item."""
    
    try:
        with DatabaseQueryTimer():
            new_item = ItemService.create(db, item_data)
        
        items_operations_total.labels(operation='create', status='success').inc()
        return new_item
    except Exception as e:
        items_operations_total.labels(operation='create', status='error').inc()
        raise


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    """Met à jour un item existant."""
    
    try:
        with DatabaseQueryTimer():
            item = ItemService.update(db, item_id, item_data)
        
        if not item:
            items_operations_total.labels(operation='update', status='not_found').inc()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        
        items_operations_total.labels(operation='update', status='success').inc()
        return item
    except HTTPException:
        raise
    except Exception as e:
        items_operations_total.labels(operation='update', status='error').inc()
        raise


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Supprime un item."""
    
    try:
        with DatabaseQueryTimer():
            deleted = ItemService.delete(db, item_id)
        
        if not deleted:
            items_operations_total.labels(operation='delete', status='not_found').inc()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        
        items_operations_total.labels(operation='delete', status='success').inc()
    except HTTPException:
        raise
    except Exception as e:
        items_operations_total.labels(operation='delete', status='error').inc()
        raise
