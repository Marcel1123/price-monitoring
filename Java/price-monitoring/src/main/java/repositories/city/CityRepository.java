package repositories.city;

import entities.CityEntity;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import java.util.List;
import java.util.UUID;

@Named
@ApplicationScoped
public class CityRepository implements ICityRepository {
    @Inject
    private EntityManager entityManager;

    @Override
    public List<CityEntity> getAll() {
        return entityManager.createQuery("select c from CityEntity c").getResultList();
    }

    @Override
    public void addCity(CityEntity cityEntity) {
        EntityTransaction transaction = this.entityManager.getTransaction();
        try {
            transaction.begin();
            this.entityManager.persist(cityEntity);
        } finally {
            transaction.commit();
        }
    }

    @Override
    public CityEntity getById(UUID id) {
        return entityManager.find(CityEntity.class, id);
    }

    @Override
    public List<CityEntity> getByName(String name) {
        return entityManager.createQuery("select c from CityEntity c where c.name = :name").setParameter("name", name).getResultList();
    }

    @Override
    public List<CityEntity> getByCountry(String country) {
        return entityManager.createQuery("select c from CityEntity c where c.name = :country").setParameter("country", country).getResultList();
    }
}
