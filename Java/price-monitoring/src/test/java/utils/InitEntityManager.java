package utils;

import javax.persistence.EntityManager;
import javax.persistence.Persistence;

public class InitEntityManager {
    public static EntityManager initEntityManager(){
        return Persistence.createEntityManagerFactory("price-monitoring").createEntityManager();
    }
}
