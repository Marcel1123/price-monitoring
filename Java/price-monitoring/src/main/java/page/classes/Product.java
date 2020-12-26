package page.classes;

import entities.LocationEntity;
import lombok.Getter;
import lombok.Setter;
import repositories.location.LocationRepository;
import util.algo.find.products.DefaultProductFinder;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.faces.context.FacesContext;
import javax.inject.Inject;
import javax.inject.Named;
import java.io.IOException;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Named
@RequestScoped
@Getter
@Setter
public class Product implements Serializable {
    @Inject
    private LocationRepository locationRepository;
    @Inject
    private DefaultProductFinder productFinder;
    private List<LocationEntity> locationEntities;

    private Information information;

    @PostConstruct
    public void init(){
        information = new Information();
        locationEntities = locationRepository.getAll();
    }

    public void estimation(){
        information.getProductEntity().setLocation(locationRepository.getById(UUID.fromString(information.getLocation())));
        Map<String, Object> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getSessionMap();
        parameterValue.put("products", productFinder.prepareQuery(information));
        try {
            FacesContext.getCurrentInstance().getExternalContext().redirect("http://localhost:8080/price_monitoring_war/pages/productsFound.xhtml");
        } catch (IOException e) {
        }
    }
}
