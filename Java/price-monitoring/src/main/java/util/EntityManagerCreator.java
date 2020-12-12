package util;

import javax.enterprise.inject.Produces;
import javax.persistence.EntityManager;
import javax.persistence.Persistence;

public class EntityManagerCreator {
    @Produces
    public EntityManager create() {
        return Persistence.createEntityManagerFactory("price-monitoring").createEntityManager();
    }
}
