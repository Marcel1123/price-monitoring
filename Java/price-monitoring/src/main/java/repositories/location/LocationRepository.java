package repositories.location;

import entities.LocationEntity;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import java.util.List;
import java.util.UUID;

@Named
@ApplicationScoped
public class LocationRepository implements ILocationRepository {

    @Inject
    private EntityManager entityManager;

    @Override
    public List<LocationEntity> getAll() {
        return entityManager.createQuery("select l from LocationEntity l").getResultList();
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
