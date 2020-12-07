package repositories.location;

import entities.LocationEntity;
import lombok.*;

import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import java.util.List;
import java.util.UUID;

@AllArgsConstructor
public class LocationRepository implements ILocationRepository {
    private EntityManager entityManager;

    @Override
    public List<LocationEntity> getAll() {
        return null;
    }

    @Override
    public void add(LocationEntity locationEntity) {
        EntityTransaction transaction = this.entityManager.getTransaction();
        transaction.begin();
        this.entityManager.persist(locationEntity);
        transaction.commit();
    }

    @Override
    public LocationEntity getById(UUID id) {
        return entityManager.find(LocationEntity.class, id);
    }

    @Override
    public List<LocationEntity> getDistinct() {
        return entityManager.createQuery("select distinct(l.address) from LocationEntity l").getResultList();
    }

    @Override
    public List<LocationEntity> getByAddress(String address) {
        return null;
    }

    @Override
    public List<LocationEntity> getByCityId(UUID id) {
        return null;
    }
}
