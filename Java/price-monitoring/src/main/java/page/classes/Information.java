package page.classes;

import entities.LocationEntity;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import repositories.location.LocationRepository;

import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.persistence.Persistence;
import java.io.Serializable;
import java.util.List;

@ManagedBean
@SessionScoped
@Getter
@Setter
public class Information implements Serializable {
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    private LocationRepository locationRepository;

    private List<LocationEntity> locationEntities;

    @PostConstruct
    public void init(){
        locationRepository = new LocationRepository(Persistence.createEntityManagerFactory("price-monitoring").createEntityManager());
        locationEntities = locationRepository.getDistinct();
    }
}
